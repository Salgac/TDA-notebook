import pandas as pd
import numpy as np


class TEvent:
    def __init__(self, start_time, end_time, points):
        self.start_time = start_time
        self.end_time = end_time
        self.points = points

    ####################
