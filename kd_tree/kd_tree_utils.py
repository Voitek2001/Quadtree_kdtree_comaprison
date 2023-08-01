# from kd_tree.geo_types import *
from kd_tree.geo_types import *
from math import inf


def kth_smallest(arr: list, k: int, comp_ind: int) -> int:
    """
    :param arr: python list of elements
    :param k: rank k
    :return: one element of array at index k in sorted order
    """
    l, m = 0, len(arr) - 1
    while l < m:
        x = arr[k][comp_ind]
        i = l
        j = m
        while i <= j:
            while arr[i][comp_ind] < x:
                i += 1
            while arr[j][comp_ind] > x:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        if j < k:
            l = i
        if i > k:
            m = j

    return arr[k]


def get_median(arr, dimension):
    """
    :param arr:
    :param dimension: comparision index
    :return: return median of input array using kth_element
    """
    return kth_smallest(arr, (len(arr) // 2 if len(arr) & 1 else len(arr) // 2 - 1), dimension)


def get_lower_left(points: List[Point]) -> Point:
    """
    :param points:
    :return: lower left corner of set of points
    """
    lower_left = [inf] * len(points[0])
    for point in points:
        for i, el in enumerate(point):
            lower_left[i] = min(lower_left[i], el)
    return lower_left


def get_upper_right(points: List[Point]) -> Point:
    """
    :param points:
    :return: upper right corner of set of points
    """
    upper_right = [-inf] * len(points[0])
    for point in points:
        for i, el in enumerate(point):
            upper_right[i] = max(upper_right[i], el)
    return upper_right


if __name__ == '__main__':
    a = [[5], [2], [1], [9], [4], [2], [4]]
    print(kth_smallest(a, len(a) // 2, 0))
