#!/usr/bin/env python
import argparse
from .UlgExtractor import ULGExtractor
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='ULG Extractor')
    parser.add_argument('file_path', help='Path to the ULG file')
    args = parser.parse_args()
    
    extractor = ULGExtractor(args.file_path)
    data = extractor.extract_time_series()
    print(data)
    i = 0
    for topic, entries in data.items():
        timeId = 0
        timestamp = []
        values = []
        for entry in entries:
            try:
                timestamp.append(entry.get("timestamp"))
                values.append({key: value for key, value in entry.items() if key != "timestamp"})
            except Exception as e:
                print(f"Debug: Could not unpack entry {entry} due to error: {e}")

        series_data = {}
        for d in values:
            for key, val in d.items():
                if "timestamp" not in key: 
                    series_data.setdefault(key, []).append(val)

        for key, series in series_data.items():
            plt.plot(timestamp, series, label=key)

        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.title(topic)
        plt.legend()
        plt.show()
        i = i+1
        if i==2: break

if __name__ == '__main__':
    main()