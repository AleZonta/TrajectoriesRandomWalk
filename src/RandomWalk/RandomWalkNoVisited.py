"""
TLSTM. Turing Learning system to generate trajectories
Copyright (C) 2018  Alessandro Zonta (a.zonta@vu.nl)

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


def random_walk_standard(apf, start, distance_target, pre_matrix):
    already_visited = {}
    # start from the first point
    final_trajectory = [start]
    already_visited["{}-{}".format(start.x, start.y)] = 1

    current_node = start
    # generate distance_target steps
    for step in range(distance_target):
        # Generate children
        points = list_neighbours(x_value=current_node.x, y_value=current_node.y, apf=apf)
        points_on_the_street = pre_matrix.keep_only_points_on_street(points=points)

        # check if nodes are already visited
        real_points_on_the_street = [node for node in points_on_the_street if "{}-{}".format(node.x, node.y) not in already_visited]

        # random walk, select randomly where to go
        index_max = np.random.random_integers(low=0, high=len(real_points_on_the_street))
        current_node = real_points_on_the_street[index_max]
        final_trajectory.append(current_node)
        already_visited["{}-{}".format(current_node.x, current_node.y)] = 1
