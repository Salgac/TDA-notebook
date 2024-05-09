from datetime import datetime

import TWeather as weather


class TEvent:

    def __init__(self, start_time, end_time, vehicle, points):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = 0
        self.vehicle = vehicle
        self.points = points

        # weather
        w = weather.byTimestamp(self.start_time)
        self.weather = {
            key: w[key]
            for key in [
                "conditions",
                "temp",
                "precip",
                "dew",
                "humidity",
                "windspeed",
                "visibility",
            ]
            if key in w
        }

    ####################
    def get_popup(self):
        return f"""
                <table style="width: 150px;">
                    <tr>
                        <td>Date:</td>
                        <td>{self.date_s()}</td>
                    </tr>
                    <tr>
                        <td>Time:</td>
                        <td>{self.time_diff_s()}</td>
                    </tr>
                    <tr>
                        <td>Duration:</td>
                        <td>{self.get_duration()}s</td>
                    </tr>
                    <tr>
                        <td>Line:</td>
                        <td>{normalize_line(self.points[0][4])}</td>
                    </tr>
                    <tr>
                        <td>Vehicle:</td>
                        <td>{self.vehicle}</td>
                    </tr>
                    <tr>
                        <td>Points:</td>
                        <td>{len(self.points)}</td>
                    </tr>
                    <tr>
                        <td>Speed:</td>
                        <td>{self.speed_s()}</td>
                    </tr>
                    <tr>
                        <td>Diff:</td>
                        <td>{self.speed_diff()}</td>
                    </tr>
                    <tr>
                        <td>Weather:</td>
                        <td>{self.weather_detail()}</td>
                    </tr>
                </table>
                """

    def get_title(self):
        return f"{self.vehicle}, {normalize_line(self.points[0][4])}, {self.date_s()} {self.time_diff_s()}"

    def get_filename(self):
        return f"{self.vehicle}_{self.date_s()}_{self.start_s()}"

    def time_diff_s(self):
        return f"{self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}"

    def date_s(self):
        return self.start_time.strftime("%d.%m.%Y")

    def start_s(self):
        return self.start_time.strftime("%H:%M:%S")

    def speed_s(self):
        return f"{self.points[0][3]} - {self.points[-1][3]}"

    def speed_diff(self):
        return self.points[0][3] - self.points[-1][3]

    def weather_detail(self):
        w = self.weather
        return f"{w['conditions']}, {w['temp']}°C, {w['precip']}mm"

    def get_duration(self):
        self.duration = (self.end_time - self.start_time).total_seconds()
        return self.duration


def normalize_line(line):
    l = line
    try:
        l = int(line)
    except:
        None
    return l
