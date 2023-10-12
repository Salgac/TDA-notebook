import pandas as pd
import numpy as np


class TDataFrame:
    def __init__(self, filename, df):
        self.df = df
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
        self.ll = df.get(
            [
                "IS_Latitude",
                "IS_Longitude",
                "NudzBr_1",
                "Time",
                "Velocity",
                "IS_Cislo_sluzby",
            ]
        ).dropna()

        emb = self.ll.loc[df["NudzBr_1"] == 1]
        self.emb = list(
            zip(
                emb["IS_Latitude"],
                emb["IS_Longitude"],
                emb["Time"],
                emb["Velocity"],
                emb["IS_Cislo_sluzby"],
            )
        )

        # self.bell = list(self.ll.loc[df['NudzBr_1'] == 1].drop(columns=['NudzBr_1']).to_records(index=False))

    # getters
    def get_lls(self, input):
        output = []
        for i in input:
            output.append((i[0], i[1]))
        return output

    def get_popups(self, input):
        output = []
        for i in input:
            output.append(
                f"Date: {self.date}<br>Time: {i[2]}<br>Line: {i[4]}<br>Vehicle: {self.vehicle}<br>Velocity: {i[3]}"
            )
        return output
