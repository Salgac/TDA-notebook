from datetime import datetime
import pandas as pd

# load all data
event_data = pd.read_csv("data/exports/events_all.csv")
event_data["start_time"] = pd.to_datetime(event_data["start_time"])
event_data["hour"] = event_data["start_time"].dt.floor("h")
event_counts = event_data.groupby("hour").size().reset_index(name="event_count")

# load critical data
event_fil_data = pd.read_csv("data/exports/events_filtered.csv")
event_fil_data["start_time"] = pd.to_datetime(event_fil_data["start_time"])
event_fil_data["hour"] = event_fil_data["start_time"].dt.floor("h")
event_fil_counts = (
    event_fil_data.groupby("hour").size().reset_index(name="critical_event_count")
)

# weather data
weather_data = pd.read_csv("data/bratislava 2022-10-01 to 2022-10-31.csv")
weather_data["datetime"] = pd.to_datetime(weather_data["datetime"])
weather_data["hour"] = weather_data["datetime"].dt.floor("h")

# merge
weather_data = weather_data.merge(event_counts, on="hour", how="left")
weather_data = weather_data.merge(event_fil_counts, on="hour", how="left")

# cleanup
weather_data.drop(columns=["hour"], inplace=True)
weather_data["event_count"].fillna(0, inplace=True)
weather_data["event_count"] = weather_data["event_count"].astype(int)
weather_data["critical_event_count"].fillna(0, inplace=True)
weather_data["critical_event_count"] = weather_data["critical_event_count"].astype(int)

# save and print total event count
weather_data.to_csv("data/exports/weather_with_events.csv", index=False)

print(event_counts["event_count"].sum())
print(event_fil_counts["critical_event_count"].sum())
