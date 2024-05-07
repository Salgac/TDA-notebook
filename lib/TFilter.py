from datetime import datetime
import TWeekDay as twd


def filter_tdfs(tdfs, line, date, weekday, vehicle):
    # line
    l1, l2, l3 = line
    data = tdfs if l1 == "*" else [df for df in tdfs if str(df.line_num) == l1]
    data = data if l2 == "*" else [df for df in data if str(df.line_order) == l2]
    data = data if l3 == "*" else [df for df in data if str(df.line_mode) == l3]

    # dates
    d1, d2 = map(lambda date_str: datetime.strptime(date_str, "%d.%m.%Y"), date)
    data = list(filter(lambda df: d1 <= df.date <= d2, data))

    # weekday
    data = (
        data
        if weekday == twd.TWeekDay.ALL
        else [
            df for df in tdfs if df.date.strftime("%A") == twd.Mapper.get(weekday, "")
        ]
    )

    # vehicle
    data = data if vehicle == "*" else [df for df in data if df.vehicle == vehicle]

    return data
