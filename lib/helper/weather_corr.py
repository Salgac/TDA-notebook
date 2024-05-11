import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

# read weather data
df = pd.read_csv("data/exports/weather_with_events.csv")

corr_matrix = df.corr(numeric_only=True)[
    ["event_count", "critical_event_count"]
].sort_values(by="event_count", ascending=False)

# corr heatmap
heatmap = sn.heatmap(corr_matrix, vmin=-1, vmax=1, annot=True, cmap="BrBG")
plt.figure(figsize=(16, 6))
heatmap.set_title(
    "Features Correlating with Events count", fontdict={"fontsize": 12}, pad=12
)

# save
plt.savefig("data/img/event_correlation.png", dpi=300, bbox_inches="tight")
plt.show()
