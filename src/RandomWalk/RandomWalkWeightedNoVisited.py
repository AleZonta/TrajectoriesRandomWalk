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

from src.Utils.Funcs import list_neighbours, _standard_normalisation


def random_walk_weighted_no_visited(apf, start, distance_target, pre_matrix, genome, K):
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
        real_points_on_the_street = [node for node in points_on_the_street if
                                     "{}-{}".format(node.x, node.y) not in already_visited]

        if len(real_points_on_the_street) == 0:
            break
        total_charges = [pre_matrix.return_charge_from_point(current_position=node, genome=genome, K=K) for node in real_points_on_the_street]

        total_charges_normalised = [_standard_normalisation(old_value=el, old_min=min(total_charges),
                                                            old_max=max(total_charges), new_min=0, new_max=1)
                                    for el in total_charges]
        total_charges = [el / sum(total_charges_normalised) for el in total_charges_normalised]

        # random walk, select randomly where to go
        current_node = np.random.choice(a=real_points_on_the_street, size=1, p=total_charges)[0]
        final_trajectory.append(current_node)
        already_visited["{}-{}".format(current_node.x, current_node.y)] = 1

    return final_trajectory
