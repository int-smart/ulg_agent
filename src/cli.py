#!/usr/bin/env python
import argparse
from extractor.UlgExtractor import ULGExtractor
import matplotlib.pyplot as plt
from core.providers.together import TogetherAI
import json
from core.processor.chunking import NumpyEncoder, ChunkProcessor

def process_data(client, chunkProcessor, data, heuristics):
    """Process data chunks and aggregate summaries"""
    chunks = chunkProcessor.chunk_json_data(data, 250)
    client.set_system_prompt(heuristics)
    summary = client.summarize_data(chunks)
    return summary
    
def plot(values):
    pass
    # for key, series in values.items():
    #     if key != 'timestamp':
    #         plt.plot(values['timestamp'], series, label=key)

    # plt.xlabel("Timestamp")
    # plt.ylabel("Value")
    # plt.title(topic)
    # plt.legend()
    # plt.show()

def main():
    parser = argparse.ArgumentParser(description='ULG Extractor')
    parser.add_argument('file_path', help='Path to the ULG file')
    parser.add_argument('--heuristics', help='Path to heuristics data')
    args = parser.parse_args()
    
    extractor = ULGExtractor(args.file_path)
    chunkProcessor = ChunkProcessor()
    client = TogetherAI()
    data = extractor.extract_time_series()
    heuristics_data = ""
    if args.heuristics:
        with open(args.heuristics, 'r', encoding='utf-8') as f:
            heuristics_data = f.read()

    i = 0
    for topic, entries in data.items():
        values = {key: [d[key] for d in entries] for key in entries[0].keys()}
        if topic == "actuator_armed":
            json_data = json.dumps(values, cls=NumpyEncoder)
            summary = process_data(client, chunkProcessor, json_data, heuristics_data)
            print(summary)        
            break

if __name__ == '__main__':
    main()