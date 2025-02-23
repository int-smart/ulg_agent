#!/usr/bin/env python
import argparse
from extractor.UlgExtractor import ULGExtractor
import matplotlib.pyplot as plt
from core.providers.together import TogetherAI
import json
from core.processor.chunking import NumpyEncoder, ChunkProcessor
from core.processor.plotter import Plotter

def process_data(client, chunkProcessor, data, heuristics):
    """Process data chunks and aggregate summaries"""
    chunks = chunkProcessor.chunk_json_data(data, 250)
    client.set_heuristics(heuristics)
    summary = client.summarize_data(chunks)
    return summary
    
def plot(topic, values):
    for key, series in values.items():
        if 'timestamp' not in key:
            plt.plot(values['timestamp'], series, label=key)

    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.title(topic)
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='ULG Extractor')
    parser.add_argument('file_path', help='Path to the ULG file')
    parser.add_argument('--heuristics', help='Path to heuristics data')
    args = parser.parse_args()
    
    extractor = ULGExtractor(args.file_path)
    chunkProcessor = ChunkProcessor()
    client = TogetherAI()
    data = extractor.extract_time_series()
    plotter = Plotter()

    heuristics_data = ""
    if args.heuristics:
        with open(args.heuristics, 'r', encoding='utf-8') as f:
            heuristics_data = json.load(f)

    values = {}
    for topic, entries in data.items():
        values[topic] = {key: [d[key] for d in entries] for key in entries[0].keys()}

    plots = []
    for key in heuristics_data["comparison_topics"].keys():
        plotter.plot_topics(values, heuristics_data["comparison_topics"][key])
        plots.append(plotter.convert_plot_to_image())
    
    client.summarize_plots(plots)
    # if topic == "estimator_states":
    #     plotter.plot_topics(topic, values)
    #     # json_data = json.dumps(values, cls=NumpyEncoder)
    #     # summary = process_data(client, chunkProcessor, json_data, heuristics_data)
    #     # print(f"\n{summary}\n")            
    #     break

if __name__ == '__main__':
    main()