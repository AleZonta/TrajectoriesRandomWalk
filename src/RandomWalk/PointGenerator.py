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
from src.RandomWalk.RandomWalkFitness import random_walk_weighted_fitness
from src.RandomWalk.RandomWalkFitnessNoVisited import random_walk_weighted_fitness_no_visited
from src.RandomWalk.RandomWalkNoVisited import random_walk_no_visited
from src.RandomWalk.RandomWalkStandard import random_walk_standard
from src.RandomWalk.RandomWalkWeighted import random_walk_weighted
from src.RandomWalk.RandomWalkWeightedNoVisited import random_walk_weighted_no_visited


class PointGenerator(object):
    """
    Proxy class for the method used to generate the path
    """

    def __init__(self, typology_needed, pre_matrix):
        self._type = typology_needed
        self.pre_matrix = pre_matrix

    def get_path(self, total_distance, genome, K, current_node, apf):
        """
        Return the path with the method chosen to use
        :param total_distance:  total distance to travel
        :param genome: genome
        :param K: constant for the computation of the charge
        :param current_node: current node
        :param apf: apf
        :return: path generated
        """
        if self._type == 0:
            return random_walk_standard(apf=apf, start=current_node, distance_target=total_distance,
                                        pre_matrix=self.pre_matrix)
        elif self._type == 1:
            return random_walk_no_visited(apf=apf, start=current_node, distance_target=total_distance,
                                          pre_matrix=self.pre_matrix)
        elif self._type == 2:
            return random_walk_weighted(apf=apf, start=current_node, distance_target=total_distance,
                                        pre_matrix=self.pre_matrix, genome=genome, K=K)
        elif self._type == 3:
            return random_walk_weighted_no_visited(apf=apf, start=current_node, distance_target=total_distance,
                                                   pre_matrix=self.pre_matrix, genome=genome, K=K)
        elif self._type == 4:
            return random_walk_weighted_fitness(apf=apf, start=current_node, distance_target=total_distance,
                                                pre_matrix=self.pre_matrix, genome=genome, K=K)
        elif self._type == 5:
            return random_walk_weighted_fitness_no_visited(apf=apf, start=current_node, distance_target=total_distance,
                                                           pre_matrix=self.pre_matrix, genome=genome, K=K)
        else:
            raise ValueError("type not implemented")
