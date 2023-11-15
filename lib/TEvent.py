class TEvent:
    def __init__(self, start_time, end_time, points):
        self.start_time = start_time
        self.end_time = end_time
        self.points = points

    ####################
    def get_popup(self):
        return f"""
                {self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}\n
                Points: {len(self.points)}\n
                Speed: {self.points[0][3]} - {self.points[-1][3]}
                """
