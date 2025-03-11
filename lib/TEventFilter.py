import pandas as pd
from datetime import datetime

from TEvent import TEvent
import TWeather as weather
import TWeatherType as twt


def detect_events(data):
    # for each TDataFrame extract events
    time_window = pd.Timedelta(seconds=10)
    events = []
    for d in data:
        current_event = None
        for record in d.rows_filtered:
            # Extract into TEvent
            timestamp = record[2]

            try:
                timestamp = pd.Timestamp(timestamp)  # Ensures it's a valid datetime

                if (
                    current_event is None
                    or current_event.end_time > timestamp
                    or (timestamp - current_event.end_time) > time_window
                ):
                    # Start a new event
                    current_event = TEvent(timestamp, timestamp, d.vehicle, [record])
                    events.append(current_event)
                else:
                    # Add to the current event
                    current_event.points.append(record)
                    current_event.end_time = timestamp

            except Exception as e:
                print(f"🚨 Skipping invalid timestamp: {timestamp} → {e}")
                continue  # Skip this record

    return events


def filter_zero(events):
    return [event for event in events if not event.points[0][3] == 0]


def filter_diff(events, limit):
    return [event for event in events if event.speed_diff() >= limit]


def filter_embs(events):
    return [event for event in events if event.points[-1][3] == 0]


def filter_time(events, time):
    # filter rows by time
    t1, t2 = map(lambda time_str: datetime.strptime(time_str, "%H:%M:%S").time(), time)
    return [
        event
        for event in events
        if (t1 <= event.start_time.time()) & (event.start_time.time() <= t2)
    ]


def filter_weather(events, type):
    return [
        event
        for event in events
        if get_weather_type(type)
        in (weather.byTimestamp(event.points[0][2])["conditions"]).split(", ")
    ]


def get_weather_type(type):
    return twt.Mapper.get(type, "")
