import pandas as pd

weather_data = pd.read_csv("data/bratislava 2022-10-01 to 2022-10-31.csv")


def round_to_nearest_hour(timestamp):
    if timestamp.minute >= 30:
        rounded_dt = timestamp.replace(
            hour=timestamp.hour + 1, minute=0, second=0, microsecond=0
        )
    else:
        rounded_dt = timestamp.replace(minute=0, second=0, microsecond=0)
    return rounded_dt.isoformat()


def byTimestamp(timestamp):
    rounded_timestamp = round_to_nearest_hour(timestamp)

    filtered_data = weather_data[weather_data["datetime"] == rounded_timestamp]
    result = filtered_data.to_dict("records")[0] if not filtered_data.empty else None

    return result
