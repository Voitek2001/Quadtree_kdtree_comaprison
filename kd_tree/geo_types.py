from typing import Tuple, List

Point = List[float]

class Rectangle:
    def __init__(self, lower_left: Point, upper_right: Point):
        self.lower_left = lower_left
        self.upper_right = upper_right

    def __str__(self):
        return "Prostokąt" + " LL= " + str(self.lower_left) + " UR= " + str(self.upper_right)
