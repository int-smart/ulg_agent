from together import Together
from dotenv import load_dotenv
import os

load_dotenv()  # load variables from .env
API_KEY = os.getenv("TOGETHER_API_KEY")

class TogetherAI:
    def __init__(self, reasoning_model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B", vision_model="meta-llama/Llama-Vision-Free"):
        self.client = Together(api_key=API_KEY)
        self.reasoning_model = reasoning_model
        self.vision_model = vision_model
        self.heuristics = None

    def set_heuristics(self, heuristics):
        self.heuristics = heuristics

    def get_response(self, model, messages, streamResponse=False):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=streamResponse
        )

        response = ""
        if streamResponse:
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""
        else:
            response = completion.choices[0].message.content

        return response

    def build_messages(self, prompt, system_prompt, image, history=[]):
        messages = history.copy()
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        if image:
            messages.append(
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image}"
                            }
                        }
                    ]
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )        
        return messages
  
    def summarize_data(self, chunks):
        summaries = []
        # Process each chunk
        for chunk in chunks:
            print("Chunk is of size ",len(chunk))
            messages=self.build_messages(
                f"What can you infer about the flight from this log section{' given ' + ' '.join(summaries) if len(summaries) > 0 else ''}:\n{chunk}", 
                f"Analyze this log chunk and provide key insights. If this is a continuation, maintain context from previous summaries. {f'Please make sure of the following: {self.heuristics}' if self.heuristics else ''}", 
                None,
                history=[])
            response = self.get_response(self.reasoning_model, messages)
            print("messages are ", messages)
            summaries.append(response)
        print('\n'.join(summaries))        # Final synthesis of all summaries
        if len(summaries) > 1:
            messages=self.build_messages(
                "Combine these summary insights into a complete analysis:\n" + "\n".join(summaries),
                "Synthesize these summaries into a coherent analysis",
                None,
                history=[],
            )
            final_completion = self.get_response(self.reasoning_model, messages)
            return final_completion
        return summaries[0]
    
    def summarize_plots(self, plots):
        summaries = []
        # Process each chunk
        for plot in plots:
            messages=self.build_messages(
                f"What can you infer about the flight from this plot {' given ' + ' '.join(summaries) if len(summaries) > 0 else ''}", 
                f"Analyze this log plot and provide key insights. If this is a continuation, maintain context from previous summaries. {f'Please make sure of the following: {self.heuristics}' if self.heuristics else ''}", 
                plot,
                history=[])
            print("messages are ", messages)
            response = self.get_response(self.vision_model, messages)
            summaries.append(response)
        print('\n'.join(summaries))        # Final synthesis of all summaries
        if len(summaries) > 1:
            messages=self.build_messages(
                "Combine these summary insights into a complete analysis:\n" + "\n".join(summaries),
                "Synthesize these summaries into a coherent analysis",
                None,
                history=[],
            )
            final_completion = self.get_response(self.reasoning_model, messages)
            return final_completion
        return summaries[0]