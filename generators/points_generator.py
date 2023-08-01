import math
import random
import numpy as np

from visualizer.visualizer import * 



def generate_uniform_points(n_points = 1000, square_size = 100):
    points = []
    for _ in range(n_points):
        points.append(get_random_point(square_size))
    return points


def generate_normal_points(n_points = 1000, square_size = 100):
    # Generate the points using a normal distribution
    points = np.random.normal(square_size / 2, square_size / 8, size=(n_points, 2))

    # Filter out any points that are outside the square
    points = points[(points[:,0] >= 0) & (points[:,0] < square_size) & (points[:,1] >= 0) & (points[:,1] < square_size)]

    return points.tolist()


def generate_points_on_grid(n_points = 1000, square_size = 100):
    # Set the size of the square
    square_size = 100
    dist = 100 / math.sqrt(n_points)

    # Generate the points using a grid layout
    points = np.mgrid[0:square_size:dist, 0:square_size:dist].reshape(2, -1).T

    return points.tolist()


def generate_clustered_points(n_points = 1000, square_size = 100, cluster_count = 3):
    # Generate the centers of the clusters using a uniform distribution
    cluster_centers = np.random.uniform(0, square_size, size=(cluster_count, 2))

    # Initialize an empty list to store the points
    points = []

    # Generate points for each cluster using a normal distribution
    for center in cluster_centers:
        cluster_points = np.random.normal(center, square_size / 8, size=(n_points // cluster_count, 2))
        points.append(cluster_points)

    # Concatenate all the points into a single array
    points = np.concatenate(points)

    # Filter out any points that are outside the square
    points = points[(points[:,0] >= 0) & (points[:,0] < square_size) & (points[:,1] >= 0) & (points[:,1] < square_size)]

    return points.tolist()


def generate_points_on_cross(n_points = 1000, square_size = 100):
    # Calculate the number of points needed for each line
    num_points_per_line = n_points // 2

    # Generate the points for the line parallel to the x axis
    x = np.random.uniform(0, square_size, size=num_points_per_line)
    y1 = np.full(num_points_per_line, square_size // 2)
    points_x = np.column_stack((x, y1))

    # Generate the points for the line parallel to the y axis
    x2 = np.full(num_points_per_line, square_size // 2)
    y = np.random.uniform(0, square_size, size=num_points_per_line)
    points_y = np.column_stack((x2, y))

    # Concatenate the points for the two lines into a single array
    points = np.concatenate((points_x, points_y))

    return points.tolist()


def generate_points_on_square_edges(n_points = 1000, square_size = 100):
    points = []
    for i in range(n_points):
        # Generate a random edge of the square
        edge = random.randint(0, 3)

        # Generate a random point along that edge
        if edge == 0:
            # Top edge
            x = random.uniform(0, square_size)
            y = square_size
        elif edge == 1:
            # Right edge
            x = square_size
            y = random.uniform(0, square_size)
        elif edge == 2:
            # Bottom edge
            x = random.uniform(0, square_size)
            y = 0
        else:
            # Left edge
            x = 0
            y = random.uniform(0, square_size)

        points.append((x, y))

    return points


def visualize_points(points, color = 'black'):
    plot = Plot(points=[PointsCollection(points, color=color)])
    plot.draw()


def get_random_point(square_size):
    x = random.uniform(0, square_size)
    y = random.uniform(0, square_size)
    return (x, y)