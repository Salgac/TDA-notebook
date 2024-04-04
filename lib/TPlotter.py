import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.collections import LineCollection


class TPlotter:

    def __init__(self, events) -> None:
        self.colors = {"No EMB": "green", "EMB_1": "blue", "EMB_2": "red"}
        plt.rcParams["figure.figsize"] = [8, 6]
        self.events = events
        self.plots = []

    def plot(self):
        # plot speed/time per event
        for event in self.events:
            df = self.extract_data(event)

            # Create segments for LineCollection
            segments = np.column_stack((df["x_n"], df["y"]))
            segments = np.array([segments])

            # Plot each segment separately to allow different colors
            fig, ax = plt.subplots()
            for i in range(len(segments[0]) - 1):
                lc = LineCollection(
                    [segments[0][i : i + 2]],
                    colors=df["colors"][i : i + 2],
                    linewidth=2,
                )
                ax.add_collection(lc)

            # Plot the LineCollection
            ax.margins(0.1)

            # Segment the data based on 'slip' changes
            segments = []
            start_idx = 0
            for i in range(1, len(df)):
                if df["Slip"][i] != df["Slip"][i - 1]:
                    segments.append((start_idx, i - 1))
                    start_idx = i
            segments.append((start_idx, len(df) - 1))

            # Plot each segment separately with corresponding background color
            for seg_start, seg_end in segments:
                seg_df = df.iloc[seg_start : seg_end + 1]
                color = "red" if seg_df["Slip"].iloc[0] == 1 else "none"
                plt.fill_between(seg_df["x"], 0, plt.ylim()[1], color=color, alpha=0.1)

            # Set plot labels and title
            plt.xlabel("Time")
            plt.ylabel("Speed (km/h)")
            plt.title("Event: " + event.get_title())
            plt.ylim(0, 55)
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

            ax.legend(handles=self.legend())

            # Show the plot
            plt.tight_layout()

            self.plots.append(plt.gcf())
            plt.show()

    def save(self):
        # save
        for plot, event in zip(self.plots, self.events):
            plot.savefig(
                f"data/img/plt_{event.get_filename()}.png", bbox_inches="tight", dpi=100
            )

    def extract_data(self, event):
        # extract data
        x = [lst[2] for lst in event.points]
        y = [lst[3] for lst in event.points]
        bell = [lst[5] for lst in event.points]
        slip = [lst[6] for lst in event.points]
        emb1 = [lst[7] for lst in event.points]
        emb2 = [lst[8] for lst in event.points]

        emb = []
        for e1, e2 in zip(emb1, emb2):
            if e1 == e2 == 0:
                emb.append("No EMB")
            elif e2 == 1:
                emb.append("EMB_2")
            elif e1 == 1:
                emb.append("EMB_1")

        return pd.DataFrame(
            {
                "x": x,
                "x_n": mdates.date2num(x),
                "y": y,
                "Bell": bell,
                "EMB": emb,
                "Slip": slip,
                "colors": pd.Series(emb).map(self.colors),
            }
        )

    def legend(self):
        # Create legend
        fill_handle = plt.Rectangle(
            (0, 0), 1, 1, fc="red", alpha=0.1, label="Slip / Slide"
        )
        legend_handles = [
            plt.Line2D([0, 1], [0, 1], color=color, linewidth=2, label=label)
            for label, color in self.colors.items()
        ]
        return legend_handles + [fill_handle]
