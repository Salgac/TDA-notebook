import pandas as pd
import time


def filter_tdfs(dfs, line, date):
    # filter dfs by every setting
    filtered = dfs if line == "*" else [df for df in dfs if df.line_num == line]

    # dates
    d1, d2 = map(lambda date_str: time.strptime(date_str, "%d.%m.%Y"), date)
    filtered = list(
        filter(lambda df: d1 <= time.strptime(df.date, "%d.%m.%Y") <= d2, filtered)
    )

    return filtered
