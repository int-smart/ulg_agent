import io
import base64
import matplotlib.pyplot as plt
from PIL import Image

class Plotter:
    """
    A class to plot PX4 ULG metrics from multiple topics and convert
    the resulting figure to an image.
    """

    def __init__(self):
        # Optionally store any configuration here
        pass

    def plot_topics(
        self,
        data_dict,
        metrics_to_compare,
        title="Comparison Plot",
        x_label="Timestamp",
        y_label="Metric Value"
    ):
        """
        Plot metrics from data_dict on the same figure.

        :param data_dict: dict where keys are topic names and values are dictionaries
                          containing 'timestamp' and the metric series, e.g.:
                          {
                            "topic1": {
                              "timestamp": [...],
                              "pos_x": [...],
                              "pos_setpoint_x": [...]
                            },
                            "topic2": {
                              "timestamp": [...],
                              "vel_x": [...],
                              ...
                            },
                            ...
                          }
        :param metrics_to_compare: list of (topic, metric) tuples to compare on one figure.
                                  Example: [("vehicle_local_position", "pos_x"),
                                            ("vehicle_local_position_setpoint", "pos_x_setpoint")]
        :param title: Plot title
        :param x_label: Label for the x-axis
        :param y_label: Label for the y-axis
        """
        plt.figure(figsize=(8, 5))

        # Assume all topics share a (roughly) comparable timestamp scale 
        for topic, metric in metrics_to_compare:
            if topic not in data_dict:
                print(f"Warning: {topic} not found in data_dict.")
                continue
            
            topic_data = data_dict[topic]
            if "timestamp" not in topic_data:
                print(f"Warning: no timestamp in data for {topic}.")
                continue
            if metric not in topic_data:
                print(f"Warning: metric {metric} not found in {topic}.")
                continue
            
            timestamps = topic_data["timestamp"]
            values = topic_data[metric]
            plt.plot(timestamps, values, label=f"{topic}/{metric}")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def convert_plot_to_image(self):
        """
        Convert the currently active matplotlib figure to a base64 encoded string.
        Returns:
            A base64 encoded string of the plot image.
        """
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)  # Adjust DPI as desired
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return img_str