import pandas as pd


def filter_tdfs(dfs, line):
    # filter dfs by every setting
    filtered = dfs if line == "*" else [df for df in dfs if df.line_num == line]

    return filtered


def extract_ll(data):
    # create an array of points
    lat_lon = []

    for tdf in data:
        for c in tdf.emb:
            # lat_lon.append((c[0], c[1], f"Line {tdf.line}"))
            lat_lon.append(f"POINT ({c[0]} {c[1]})")

    return lat_lon
