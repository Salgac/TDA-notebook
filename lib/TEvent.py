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
                <div style="width: 150px;">
                    Date: {time.strftime('%d.%m.%Y',self.date)}<br>
                    Time: {self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}<br>
                    Line: {int(self.points[0][4])}<br>
                    Vehicle: {self.vehicle}<br>
                    Points: {len(self.points)}<br>
                    Speed: {self.points[0][3]} - {self.points[-1][3]}<br>
                    Diff: {self.speed_diff()}<br>
                </div>
                """

    def speed_diff(self):
        return self.points[0][3] - self.points[-1][3]
