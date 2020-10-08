import math


def distance_from(_location, location):
    return math.ceil(math.hypot(location[0] - _location[0], location[1] - _location[1]))
