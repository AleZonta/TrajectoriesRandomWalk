"""
TrajectoriesRandomWalk. Towards a human-like movements generator based on environmental features
Copyright (C) 2020  Alessandro Zonta (a.zonta@vu.nl)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
from scipy.spatial import distance

from src.Helpers.Fitness.ValueGraphFitness import get_fitness_value
from src.Utils.Point import Point


def list_neighbours(x_value, y_value, apf, list_already_visited=None):
    """
    Return all the neighbours cells.
    If the neighbour is already visited, it is removed from the return list
    :param x_value: x value starting point
    :param y_value: y value starting point
    :param list_already_visited: list of point already visited
    :return: list of neighbours
    """
    xx = [x_value - 1, x_value, x_value + 1, x_value + 1, x_value + 1, x_value, x_value - 1, x_value - 1]
    yy = [y_value + 1, y_value + 1, y_value + 1, y_value, y_value - 1, y_value - 1, y_value - 1, y_value]

    # remove negative values and values outside bounds apf
    to_erase_x = []
    for i in range(len(xx) - 1, -1, -1):
        if xx[i] < 0:
            to_erase_x.append(i)
        if xx[i] >= apf[0]:
            to_erase_x.append(i)
    to_erase_y = []
    for i in range(len(yy) - 1, -1, -1):
        if yy[i] < 0:
            to_erase_y.append(i)
        if yy[i] >= apf[1]:
            to_erase_x.append(i)

    for i in range(len(xx) - 1, -1, -1):
        erase = False
        if i in to_erase_x or i in to_erase_y:
            erase = True
        if erase:
            del xx[i]
            del yy[i]

    points = []
    for i in range(len(xx)):
        p = Point(xx[i], yy[i])
        if not is_in_list(list_of_points=list_already_visited, point_to_check=p):
            points.append(p)
    return points


def is_in_list(list_of_points, point_to_check):
    """
    Check if a point is already in the list.
    If the list of points is empty or not used, the functions returns False

    :param list_of_points: list of points where to check
    :param point_to_check: point to check
    :return: Boolean Value: True if it is in the list, False otherwise
    """
    if list_of_points is None:
        return False
    for el in list_of_points:
        if el.equals(p1=point_to_check):
            return True
    return False


def _get_direction(current_point, next_point):
    """
    From the current point return the vector defining the decision the model follow to move to the next point
    :param current_point: current location
    :param next_point: point just moved on
    :return: vector specifying the decision the model made to go to the next point. Vector 8 positions one-hot encoded
    """
    x_value = int(current_point.x)
    y_value = int(current_point.y)
    x_value_next = int(next_point.x)
    y_value_next = int(next_point.y)

    diff_x = x_value_next - x_value
    diff_y = y_value_next - y_value
    if diff_x == 1 and diff_y == -1:
        return [1, 0, 0, 0, 0, 0, 0, 0]
    elif diff_x == 0 and diff_y == -1:
        return [0, 1, 0, 0, 0, 0, 0, 0]
    elif diff_x == -1 and diff_y == -1:
        return [0, 0, 1, 0, 0, 0, 0, 0]
    elif diff_x == -1 and diff_y == 0:
        return [0, 0, 0, 1, 0, 0, 0, 0]
    elif diff_x == -1 and diff_y == 1:
        return [0, 0, 0, 0, 1, 0, 0, 0]
    elif diff_x == 0 and diff_y == 1:
        return [0, 0, 0, 0, 0, 1, 0, 0]
    elif diff_x == 1 and diff_y == 1:
        return [0, 0, 0, 0, 0, 0, 1, 0]
    elif diff_x == 1 and diff_y == 0:
        return [0, 0, 0, 0, 0, 0, 0, 1]
    else:
        raise Exception("{} and {} not present".format(diff_x, diff_y))


def compute_fintess_trajectory(tra_moved_so_far):
    """
    Compute the fitness of the current trajectory
    :param tra_moved_so_far: points of the trajectory
    :return: total fitness value and single fitness component
    """
    # now I have trajectory and direction, need to compute the fitness
    # as distance I am using the number of timesteps of the trajectories
    total_length = len(tra_moved_so_far)
    directions = [_get_direction(current_point=tra_moved_so_far[ii - 1], next_point=tra_moved_so_far[ii])
                  for ii in range(1, len(tra_moved_so_far))]
    # compute the curliness of the tra
    distances = [distance.euclidean(directions[j - 1], directions[j]) for j in range(1, len(directions))]
    if len(distances) > 0:
        curliness = np.mean(np.array(distances))
        if np.isnan(curliness):
            curliness = 0.0
    else:
        curliness = 0.0
    vector_distances = []
    if len(tra_moved_so_far) > 0:
        starting_point = [tra_moved_so_far[0].x, tra_moved_so_far[0].y]
        # compute distance to further point
        vector_distances = [distance.cityblock(starting_point, [tra_moved_so_far[idx].x, tra_moved_so_far[idx].y]) for
                            idx
                            in range(1, len(tra_moved_so_far) - 1)]

    if len(vector_distances) > 0:
        further_distance_to_point = max(vector_distances)
    else:
        further_distance_to_point = 0

    distance_to_middle_point = 0
    distance_to_end_point = 0
    if len(tra_moved_so_far) > 0:
        starting_point = [tra_moved_so_far[0].x, tra_moved_so_far[0].y]
        # compute distance to middle point
        middle_point = tra_moved_so_far[int(len(tra_moved_so_far) / 2)]
        distance_to_middle_point = distance.cityblock(starting_point, [middle_point.x, middle_point.y])
        # compute distance to end
        end_point = tra_moved_so_far[len(tra_moved_so_far) - 1]
        distance_to_end_point = distance.cityblock(starting_point, [end_point.x, end_point.y])

    out, _, _, _ = get_fitness_value(length=total_length, curliness=curliness,
                                     further_distance=further_distance_to_point)
    return out, [total_length, curliness, further_distance_to_point, distance_to_middle_point, distance_to_end_point]


def compute_charge_points(genome, current_position, K, pre_matrix):
    """
    Compute the attraction of the points
    :param genome: genome
    :param genome_meaning: meaning if every pos of the genome
    :param values_matrix: values to translate cells to coordinates
    :param current_position: current position
    :param K: constant for the computation of the charge
    :param pre_matrix: pre computation of distance from the cell to the objects
    :return: total charge
    """
    # now prematrix is the cell system optimised
    # start_time = time.time()
    total_charge = pre_matrix.return_charge_from_point(current_position=current_position, genome=genome, K=K)
    # current_time = time.time()
    # time_from_start = current_time - start_time  # time in seconds
    # print(time_from_start)
    return total_charge


def keep_only_points_on_street(apf, points):
    """
    Check if the points provided are on a route
    :param apf: Dataframe describing the routing system
    :param points: list of points to check
    :return: list of points from the input list that are actually on a route
    """
    points_on_street = []
    for p in points:
        # print("{}-{} -> {}".format(int(p.x), int(p.y), apf.iloc[int(p.x)][int(p.y)]))
        if apf.iloc[int(p.x)][int(p.y)] != 0:
            points_on_street.append(p)
    return points_on_street


def _standard_normalisation(old_value, old_min, old_max, new_min, new_max):
    """
    Normalisation function
    :param old_value: old value to convert
    :param old_min: old minimum
    :param old_max: old maximum
    :param new_min: new minimum
    :param new_max: new maximum
    :return: value converted in the new range
    """
    return (((old_value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
