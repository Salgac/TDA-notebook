from datetime import datetime
import pandas as pd
import ast
from geopy.distance import geodesic

import TDataType as tdt


class TDataFrame:
    def __init__(self, filename, df):
        self.df = df

        # basic data
        self.vehicle = filename.split("_")[1]

        # line data
        mode_series = df["IS_Cislo_sluzby"].mode()
        if not mode_series.empty:
            try:
                self.line = str(int(mode_series.iloc[0]))
            except:
                self.line = str(mode_series.iloc[0])
        else:
            self.line = "0000"
        try:
            self.line_num = int(self.line[0])
            self.line_order = int(self.line[1] + self.line[2])
            self.line_mode = int(self.line[3])
            self.line = int(self.line)
        except ValueError:
            self.line_num = 0
            self.line_order = 0
            self.line_mode = 0

        # date-time conversion
        self.df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
        self.df.loc[:, "Time"] = self.df["Time"].apply(
            lambda x: datetime.strptime(x, "%H:%M:%S,%f")
        )
        self.df["Timestamp"] = self.df.apply(
            lambda row: datetime.combine(row["Date"].date(), row["Time"].time()), axis=1
        )
        self.date = self.df["Date"].mode()[0]

        # geo data
        self.rows = self.df.get(
            [
                "IS_Latitude",
                "IS_Longitude",
                "NudzBr_1",
                "NudzBr_2",
                "Zvonec",
                "KolBr_1",
                "KolBr_2",
                "Sklz_Smyk",
                "Timestamp",
                "Velocity",
                "IS_Cislo_sluzby",
            ]
        ).dropna()
        self.rows_filtered = []

    ####################
    # row filters
    def filter_rows(self, type, timestamp):
        column_type = tdt.Mapper.get(type, "")

        # filter by type
        r = self.rows
        if column_type != "":
            r = r.loc[self.df[column_type] == 1]

        # filter rows by time
        t1, t2 = map(
            lambda time_str: datetime.strptime(time_str, "%H:%M:%S").time(), timestamp
        )
        r = r.loc[(t1 <= r["Timestamp"].dt.time) & (r["Timestamp"].dt.time <= t2)]

        # select relevant columns - it is a mess, but it works (afterthought)
        self.rows_filtered = list(
            zip(
                r["IS_Latitude"],
                r["IS_Longitude"],
                r["Timestamp"],
                r["Velocity"],
                r["IS_Cislo_sluzby"],
                r["Zvonec"],
                r["Sklz_Smyk"],
                r["NudzBr_1"],
                r["NudzBr_2"],
                r["KolBr_1"],
                r["KolBr_2"],
            )
        )

    def filter_zones(self, zones):
        for z in zones:
            self.rows_filtered = [
                row
                for row in self.rows_filtered
                if not geodesic(ast.literal_eval(z["coords"]), (row[0], row[1])).meters
                <= z["distance"]
            ]

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
                f"""
                <table style="width: 150px;">
                    <tr>
                        <td>Date:</td>
                        <td>{datetime.strftime('%d.%m.%Y', r[2])}</td>
                    </tr>
                    <tr>
                        <td>Time:</td>
                        <td>{datetime.strftime( '%H:%M:%S', r[2])}</td>
                    </tr>
                    <tr>
                        <td>Line:</td>
                        <td>{normalize_line(r[4])}</td>
                    </tr>
                    <tr>
                        <td>Vehicle:</td>
                        <td>{self.vehicle}</td>
                    </tr>
                    <tr>
                        <td>Speed:</td>
                        <td>{r[3]}</td>
                    </tr>
                </table>
                """
            )
        return output


def normalize_line(line):
    l = line
    try:
        l = int(line)
    except:
        None
    return l
