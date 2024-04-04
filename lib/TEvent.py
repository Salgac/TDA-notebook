from datetime import datetime


class TEvent:

    def __init__(self, start_time, end_time, vehicle, points):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = start_time - end_time
        self.vehicle = vehicle
        self.points = points

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
                </table>
                """

    def get_title(self):
        return f"{self.vehicle}, {normalize_line(self.points[0][4])}, {self.date_s()} {self.time_diff_s()}"

    def time_diff_s(self):
        return f"{self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}"

    def date_s(self):
        return self.start_time.strftime("%d.%m.%Y")

    def speed_s(self):
        return f"{self.points[0][3]} - {self.points[-1][3]}"

    def speed_diff(self):
        return self.points[0][3] - self.points[-1][3]


def normalize_line(line):
    l = line
    try:
        l = int(line)
    except:
        None
    return l
