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

import random
from haversine import haversine

from src.RandomWalk.PointGenerator import PointGenerator
from src.Utils.Point import Point
from src.Utils.RandomWrappers import random_wrapper_lognorm

K = 0.1
TIMESTEP = 1


class TrajectoryGeneration(object):
    def __init__(self, values_matrix, apf, pre_loaded_points,
                 type_of_generator, pre_matrix, genotype=None, total_distance_to_travel=5000):
        self.path = []
        self.tra = []
        self.tra_real_coordinates = []

        self.genome = genotype
        #
        self._values_matrix = values_matrix
        self._apf = apf
        self._pre_loaded_points = pre_loaded_points
        self._pre_matrix = pre_matrix
        #
        self.generator = PointGenerator(typology_needed=type_of_generator, pre_matrix=self._pre_matrix)
        self._total_distance_to_travel = total_distance_to_travel

    def create_trajectory(self, random_seed, idx):
        """
        Function that creates a trajectory from the value of the genome

        The genome contains the charge of all the objects in the map plus other information

        -> random initial point inside the area
        -> check I am in street, otherwise find closest point to the selected one in a route

        -> depending on the method chosen, generate the path

        -> transform path into trajectory
        :param random_seed: seed for random
        :param idx: index starting point
        :return:
        """
        random.seed(random_seed)
        np.random.seed(random_seed)

        self.path = []
        self.tra = []
        self.tra_real_coordinates = []
        distances = []
        while self.path is None or len(self.path) == 0:
            if self.path is None:
                self.path = []
            # adding point to path
            pre_loaded_point = self._pre_loaded_points.get_point(idx_tra=idx)
            current_node = Point(x=pre_loaded_point[0], y=pre_loaded_point[1])
            self.path.append(current_node)
            # get the path using the methodology chosen
            self.path = self.generator.get_path(total_distance=self._total_distance_to_travel,
                                                genome=self.genome, K=K,
                                                current_node=current_node, apf=self._apf.shape)

        if len(distances) == 0:
            for i in range(len(self.path) - 1):
                start = self.path[i]
                end = self.path[i + 1]
                dis = haversine((self._values_matrix[0][start.x], self._values_matrix[1][start.y]),
                                (self._values_matrix[0][end.x],
                                 self._values_matrix[1][end.y])) * 1000  # in metres
                distances.append(dis)

        # now I have the path. Need to transform it in to a trajectory
        self.tra.append(self.path[0])
        i = 0
        while i < len(self.path) - 1:
            # speed is in metres per second
            speed = random_wrapper_lognorm(mean=0, std=1)
            # space is in metres
            space = TIMESTEP * speed

            current_distance = 0
            if i >= len(distances) - 1:
                break
            while current_distance < space:
                if i >= len(distances) - 1:
                    break
                current_distance += distances[i]
                i += 1
            self.tra.append(self.path[i])

        self.tra_real_coordinates = [Point(self._values_matrix[0][p.x], self._values_matrix[1][p.y]) for p in self.tra]

        # return the distances to every points
        # now we will compute distances every time.
        # what can we use? To the nearest? To the five closest?
        # let's start distance to the nearest
        total_distances = [self._pre_matrix.return_distance_from_point(current_position=point) for point in self.tra]

        return total_distances, self.tra, self.tra_real_coordinates, self.path

    def save_trajectory_generated(self):
        """
        Store the trajectory generated on a file
        :return: string containing all the points
        """
        dic_tra_generated = {}
        for i in range(len(self.tra_real_coordinates)):
                dic_tra_generated[i] = self.tra_real_coordinates[i]
        return dic_tra_generated

    def save_raw_trajectory_generated(self):
        """
        Store the raw trajectory generated on a file
        :return: string containing all the points
        """
        dic_tra_generated = {}
        for i in range(len(self.tra)):
            dic_tra_generated[i] = self.tra[i]
        return dic_tra_generated

    def save_raw_path_generated(self):
        """
        Store the raw path generated on a file
        :return: string containing all the points
        """
        dic_tra_generated = {}
        for i in range(len(self.path)):
            dic_tra_generated[i] = self.path[i]
        return dic_tra_generated