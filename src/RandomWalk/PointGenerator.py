"""
GTEA. Turing Learning system to generate trajectories
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


class PointGenerator(object):
    """
    Proxy class for the method used to generate the path
    """
    def __init__(self, typology_needed, pre_matrix):
        if typology_needed == "weighted":
            self._type = 1
        elif typology_needed == "default":
            self._type = 0
        else:
            raise ValueError("Type requested not implemented")
        self.pre_matrix = pre_matrix

    def get_path(self, total_distance, genome, genome_meaning, values_matrix, K, distances,
                 current_node, apf, x_value):
        """
        Return the path with the method chosen to use
        :param total_distance:  total distance to travel
        :param name_and_position: name and position objects
        :param genome: genome
        :param genome_meaning: meaning if every pos of the genome
        :param values_matrix: values to translate cells to coordinates
        :param K: constant for the computation of the charge
        :param distances: vector with distances positions
        :param current_node: current node
        :param end_node: target node
        :param apf: apf
        :return: path generated
        """
        if self._type == 0:
            return
        else:
            return
