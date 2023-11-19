import pandas as pd
import geopandas as gpd

from TDataFrame import TDataFrame


class TReader:
    def __init__(self, filepaths):
        self.filepaths = filepaths

    ####################
    def read(self, limit):
        i = 0
        ltdfs = []

        for filename in self.filepaths:
            df = pd.read_csv(filename, sep=";", encoding="latin-1", low_memory=False)
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df.IS_Longitude, df.IS_Latitude),
                crs="EPSG:4326",
            )

            # add to list
            ltdfs.append(TDataFrame(filename, gdf))

            # limit
            i += 1
            if limit > 0 and i >= limit:
                break

        return ltdfs
