import pandas as pd
from datetime import datetime
from TEvent import TEvent


def detect_events(data):
    # for each TDataFrame extract events
    time_window = pd.Timedelta(seconds=10)
    events = []
    for d in data:
        current_event = None
        for record in d.rows_filtered:
            # Extract into TEvent
            timestamp = record[2]
            if (
                current_event is None
                or (timestamp - current_event.end_time) > time_window
            ):
                # Start a new event
                current_event = TEvent(
                    timestamp, timestamp, d.date, d.vehicle, [record]
                )
                events.append(current_event)
            else:
                # Add to the current event
                current_event.points.append(record)
                current_event.end_time = timestamp

    return events


def filter_zero(events):
    return [event for event in events if not event.points[0][3] == 0]


def filter_diff(events, limit):
    return [event for event in events if event.speed_diff() >= limit]


def filter_embs(events):
    return [event for event in events if event.points[-1][3] == 0]
