from together import Together
from dotenv import load_dotenv
import os

load_dotenv()  # load variables from .env
API_KEY = os.getenv("TOGETHER_API_KEY")

class TogetherAI:
    def __init__(self, model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"):
        self.client = Together(api_key=API_KEY)
        self.model = model
        self.system_prompt = None

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt

    def get_response(self, prompt):
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ""

        return response

    def summarize_data(self, chunks):
        summaries = []

        # Process each chunk
        for chunk in chunks:
            print("Chunk is of size ",len(chunk))
            temp = [
                    {"role": "system", "content": f"Analyze this log chunk and provide key insights. If this is a continuation, maintain context from previous summaries. {f'Please make sure of the following: {self.system_prompt}' if self.system_prompt else ''}"},                    
                    {"role": "user", "content": f"What can you infer about the flight from this log section{' given ' + ' '.join(summaries) if len(summaries) > 0 else ''}:\n{chunk}"},
                ]
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Analyze this log chunk and provide key insights. If this is a continuation, maintain context from previous summaries. {f'Please make sure of the following: {self.system_prompt}' if self.system_prompt else ''}"},                    
                    {"role": "user", "content": f"What can you infer about the flight from this log section{' given ' + ' '.join(summaries) if len(summaries) > 0 else ''}:\n{chunk}"},
                ]
            )
            print("messages are ", temp)
            summaries.append(completion.choices[0].message.content)
            break
        # print(summaries)

        # Final synthesis of all summaries
        if len(summaries) > 1:
            final_summary = "Combine these summary insights into a complete analysis:\n" + "\n".join(summaries)
            final_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Synthesize these summaries into a coherent analysis"},
                    {"role": "user", "content": final_summary}
                ]
            )
            return final_completion.choices[0].message.content
        
        return summaries[0]