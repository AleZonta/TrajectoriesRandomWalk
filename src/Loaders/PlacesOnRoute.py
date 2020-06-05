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

from src.Settings.args import args


class FindPlacesOnRoutes(object):
    """
    Find random places among the route system loaded in the APF.
    The previous files are only copy of the other classes present in the projects.
    This was necessary in order to have only one file running in different computer in order to make the process faster
    Did not have time to copy the entire project

    I know this is something not to do

    But for this time is okay, if comment are not present in the classes above this one, go in the project and find the
    file where that method is implemented and hopefully you will find useful comment there
    """

    def __init__(self, logger, apf=None, boundaries=None, values_matrix=None):
        self.log = logger
        self.apf = apf
        self.boundaries = boundaries
        self.values_matrix = values_matrix
        self.values = None

    def load_preloaded_position(self):
        """
        The meaning of this method is too easy to write down a useful comment.
        Instead I am loosing time writing these meaningless lines only for you that are going to read them.
        But be realistic.
        No one will ever read this comments.
        PhD hard life
        :return:
        """
        self.log.debug("Loading point already found in advance...")
        starting_point_train = np.load("{}/real_tra_test_starting_points.npy".format(args.data_path), allow_pickle=True)
        self.values = starting_point_train

    def get_point(self, idx_tra):
        first_point_str = self.values[idx_tra].split("-")
        starting_position_x = int(first_point_str[0])
        starting_position_y = int(first_point_str[1])
        return starting_position_x, starting_position_y
