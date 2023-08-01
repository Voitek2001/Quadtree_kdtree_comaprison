def get_all_except(points, excluded_indexes):
    res = []
    for i in range(len(points)):
        if i not in excluded_indexes:
            res.append(points[i])
    return res


def get_points(points, indexes):
    return [points[i] for i in indexes]