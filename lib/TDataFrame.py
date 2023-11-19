import time
from geopy.distance import geodesic

from TDataType import TDataType as tdt


class TDataFrame:
    def __init__(self, filename, df):
        self.df = df

        # basic data
        self.date = filename.split("_")[2]
        self.vehicle = filename.split("_")[1]

        # line data
        mode_series = df["IS_Cislo_sluzby"].mode()
        if not mode_series.empty:
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
        self.date = time.strptime(self.date, "%d.%m.%Y")
        self.df.loc[:, "Time"] = self.df["Time"].apply(
            lambda x: time.strptime(x, "%H:%M:%S,%f")
        )

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
    # row filters
    def filter_rows(self, type, timestamp):
        column_type = self.TDataTypeMapper.get(type, "")
        r = self.rows.loc[self.df[column_type] == 1]

        # filter rows by time
        t1, t2 = map(lambda time_str: time.strptime(time_str, "%H:%M:%S"), timestamp)
        r = r.loc[(t1 <= r["Time"]) & (r["Time"] <= t2)]

        # select relevant columns
        self.rows_filtered = list(
            zip(
                r["IS_Latitude"],
                r["IS_Longitude"],
                r["Time"],
                r["Velocity"],
                r["IS_Cislo_sluzby"],
            )
        )

    def filter_depos(self, depos):
        for depo_dict in depos:
            self.rows_filtered = [
                row
                for row in self.rows_filtered
                if not geodesic(depo_dict["c"], (row[0], row[1])).meters
                <= depo_dict["d"]
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
                        <td>{time.strftime('%d.%m.%Y', self.date)}</td>
                    </tr>
                    <tr>
                        <td>Time:</td>
                        <td>{time.strftime( '%H:%M:%S', r[2])}</td>
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
