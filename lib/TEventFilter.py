import pandas as pd
import time
from geopy.distance import geodesic
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
            timestamp = datetime.fromtimestamp(time.mktime(record[2]))
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


def filter_depo(events, settings):
    # Specify the center coordinates and radius
    center_coordinates = settings["c"]
    radius_meters = settings["d"]

    # filter
    return [
        event
        for event in events
        if not any(
            geodesic(center_coordinates, (point[0], point[1])).meters <= radius_meters
            for point in event.points
        )
    ]


def filter_zero(events):
    return [event for event in events if not event.points[0][3] == 0]


def filter_embs(events):
    return [event for event in events if event.points[-1][3] == 0]
