import time


class TEvent:
    def __init__(self, start_time, end_time, date, vehicle, points):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = start_time - end_time
        self.date = date
        self.vehicle = vehicle
        self.points = points

    ####################
    def get_popup(self):
        return f"""
                <table style="width: 150px;">
                    <tr>
                        <td>Date:</td>
                        <td>{time.strftime('%d.%m.%Y', self.date)}</td>
                    </tr>
                    <tr>
                        <td>Time:</td>
                        <td>{self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}</td>
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
                        <td>{self.points[0][3]} - {self.points[-1][3]}</td>
                    </tr>
                    <tr>
                        <td>Diff:</td>
                        <td>{self.speed_diff()}</td>
                    </tr>
                </table>
                """

    def speed_diff(self):
        return self.points[0][3] - self.points[-1][3]


def normalize_line(line):
    l = line
    try:
        l = int(line)
    except:
        None
    return l
