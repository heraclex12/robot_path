import math

class Robot():
    def __init__(self, s_a, s_b, e_a, e_b):
        self.start = (s_a, s_b)
        self.end = (e_a, e_b)

    def get_start_point(self):
        print(self.start)