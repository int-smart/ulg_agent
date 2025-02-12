import pyulog

class ULGExtractor:
    """
    Extracts time series data from a binary .ulg file using pyulog.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_time_series(self):
        """
        Extract time series data from a .ulg file, returning
        a dictionary keyed by message name with time/value data.
        """
        # Parse the ULog file (requires pip install pyulog)
        ulog = pyulog.ULog(self.file_path)

        time_series_data = {}

        # Each add_logged_messages entry stores a message name and data
        for m in ulog.data_list:
            topic_name = m.name
            data = m.data
            # Each column in data is a separate array (e.g., 'timestamp', 'x', etc.)
            # Merge them into the structure you need
            combined_rows = []
            timestamps = data['timestamp']
            for i in range(len(timestamps)):
                row = {}
                for key in data.keys():
                    row[key] = data[key][i]
                combined_rows.append(row)

            time_series_data[topic_name] = combined_rows

        return time_series_data
