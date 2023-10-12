import pandas as pd
import numpy as np

from TDataType import TDataType as tdt


class TDataFrame:
    def __init__(self, filename, df):
        self.df = df

        # basic data
        self.date = filename.split("_")[2]
        self.vehicle = filename.split("_")[1]

        # line data
        self.line = str((df.loc[:, "IS_Cislo_sluzby"]).value_counts().idxmax())
        try:
            self.line_num = int(self.line[0])
            self.line_order = int(self.line[1] + self.line[2])
            self.line_mode = int(self.line[3])
        except ValueError:
            self.line_num = 0
            self.line_order = 0
            self.line_mode = 0

        # geo data
        self.rows = df.get(
            [
                "IS_Latitude",
                "IS_Longitude",
                "NudzBr_1",
                "NudzBr_2",
                "Zvonec",
                "KolBr_1",
                "KolBr_2",
                "Sklz_Smyk",
                "Time",
                "Velocity",
                "IS_Cislo_sluzby",
            ]
        ).dropna()
        self.rows_filtered = []

        # column data filter mapper
        self.TDataTypeMapper = {
            tdt.EMB_1: "NudzBr_1",
            tdt.EMB_2: "NudzBr_2",
            tdt.TRACKB_1: "KolBr_1",
            tdt.TRACKB_2: "KolBr_2",
            tdt.BELL: "Zvonec",
            tdt.SLIP_SLIDE: "Sklz_Smyk",
        }

    ####################
    # row filter by type
    def filter_rows(self, type):
        column_type = self.TDataTypeMapper.get(type, "")
        r = self.rows.loc[self.df[column_type] == 1]

        self.rows_filtered = list(
            zip(
                r["IS_Latitude"],
                r["IS_Longitude"],
                r["Time"],
                r["Velocity"],
                r["IS_Cislo_sluzby"],
            )
        )

    ###################
    # getters
    def get_lat_lons(self):
        output = []
        for r in self.rows_filtered:
            output.append((r[0], r[1]))
        return output

    def get_popups(self):
        output = []
        for r in self.rows_filtered:
            output.append(
                f"Date: {self.date}<br>Time: {r[2]}<br>Line: {r[4]}<br>Vehicle: {self.vehicle}<br>Velocity: {r[3]}"
            )
        return output
