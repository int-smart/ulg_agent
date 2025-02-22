import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

class ChunkProcessor:
    def __init__(self, chunk_length=30000):
        self.chunk_length = chunk_length

    def chunk_text(self, text, overlap=1000):
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + self.chunk_length, text_length)
            if end < text_length:
                # Find the last newline in overlap region to avoid cutting mid-sentence
                end = text.rfind('\n', end - overlap, end) + 1
            chunks.append(text[start:end])
            start = end - overlap
        return chunks

    def chunk_json_data(self, snippet, chunk_size=10000):
        data = json.loads(snippet)
        
        # If the JSON is empty, no chunks to return
        if not data:
            return []
        
        # We'll assume all keys map to lists of the same length
        total_len = len(list(data.values())[0])
        
        chunks = []
        
        # Iterate through the data in steps of `chunk_size`
        for start_idx in range(0, total_len, chunk_size):
            end_idx = min(start_idx + chunk_size, total_len)
            
            # Build a dictionary for this chunk
            chunk_dict = {}
            for k in data.keys():
                # Slice the list for each key
                chunk_dict[k] = data[k][start_idx:end_idx]
            
            # Optionally convert the chunk to JSON
            chunk_json = json.dumps(chunk_dict)
            chunks.append(chunk_json)
        return chunks