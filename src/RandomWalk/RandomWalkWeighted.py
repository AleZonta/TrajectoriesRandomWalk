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

from src.Utils.Funcs import list_neighbours


def random_walk_weighted(apf, start, distance_target, pre_matrix, genome, K):
    """
    Generate the trajectory using the random walk weighted
    From the starting point it finds the neighbour nodes
    it checks if they are road
    get the precomputed attraction for all the nodes remaining
    normalise attraction value to be probabilities
    compute the random next node
    move to the chosen node
    repeat
    :param apf: artificial potential field, needed to check the neighbour node
    :param start: starting point
    :param distance_target: how many timestep max to generate
    :param pre_matrix: preloaded attraction values
    :param genome: multiplier for the attraction
    :param K: constant for the coulomb equation
    :return: list of nodes -> final trajectory
    """
    # start from the first point
    final_trajectory = [start]

    current_node = start
    # generate distance_target steps
    for step in range(distance_target):
        # Generate children
        points = list_neighbours(x_value=current_node.x, y_value=current_node.y, apf=apf)
        points_on_the_street = pre_matrix.keep_only_points_on_street(points=points)

        total_charges = [pre_matrix.return_charge_from_point(current_position=node, genome=genome, K=K) for node in points_on_the_street]

        total_charges = np.array([el/sum(total_charges) for el in total_charges])

        # random walk, select randomly where to go
        current_node = np.random.choice(a=points_on_the_street, size=1, p=total_charges)[0]
        final_trajectory.append(current_node)

    return final_trajectory
