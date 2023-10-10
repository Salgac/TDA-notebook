import pandas as pd


def filter_tdfs(dfs, line, date):
    # filter dfs by every setting
    filtered = dfs if line == "*" else [df for df in dfs if df.line_num == line]
    filtered = filtered if date == "*" else [df for df in filtered if df.date == date]

    return filtered
