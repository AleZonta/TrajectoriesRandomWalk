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
import logging
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm, trange
from src.Analysis.data_loader import DataLoader
from src.Loaders.LoadAPF import LoadAPF
from src.Settings.args import args


class PrintTrajectories(DataLoader):
    def __init__(self, log):
        super().__init__(log)

        self._loader_apf = LoadAPF(path=args.data_path + args.apf_name, logger=self._log)
        self._loader_apf.load_apf_only_routing_system()

    def print_paths(self, path=None, name=None, apf=False):
        """
        Print generated path on disk
        :param path: folder where to save the graphs
        :param name: name of the folder where to save the graphs
        :param apf: True if graph with Artificial Potential Field, False if only graph with trajectory
        :return:
        """
        if path is not None:
            path = "{}/{}/".format(path, name)
            os.mkdir(path)

        for idx, attraction_variant in enumerate(self._paths_generated):
            if path is not None:
                path_here = "{}/set_attraction_{}/".format(path, idx)
                os.mkdir(path_here)
            else:
                path_here = None
            for tra_idx, tra in tqdm(enumerate(attraction_variant), desc="printing trajectories variant {}".format(idx)):
                x = []
                y = []
                combinations = {}
                for points in tra:
                    x.append(int(points.x))
                    y.append(int(points.y))
                    combinations["{}-{}".format(int(points.x), int(points.y))] = 1
                max_x = max(x) + 1
                min_x = min(x) - 1
                max_y = max(y) + 1
                min_y = min(y) - 1

                max_value_x = ((max_x - min_x) + 10) * 2
                max_value_y = ((max_y - min_y) + 10) * 2

                matrix = np.zeros((max_value_x, max_value_y))

                if apf:
                    difference_to_move_x = int((max_value_x - (max_x - min_x)) / 2)
                    difference_to_move_y = int((max_value_y - (max_y - min_y)) / 2)
                    real_min_x = min_x - difference_to_move_x
                    real_max_x = max_x + difference_to_move_x
                    real_min_y = min_y - difference_to_move_y
                    real_max_y = max_y + difference_to_move_y

                    for j in range(real_min_x, real_max_x):
                        for q in range(real_min_y, real_max_y):
                            value = self._loader_apf.apf.iloc[j, q]
                            matrix_pos_x = j - real_min_x
                            matrix_pos_y = q - real_min_y
                            if "{}-{}".format(j, q) in combinations:
                                matrix[matrix_pos_x, matrix_pos_y] = 2.0
                            elif value != 0:
                                matrix[matrix_pos_x, matrix_pos_y] = 1.0
                else:
                    mdlx = int(max_value_x / 2)
                    mdly = int(max_value_y / 2)
                    for i in range(1, len(x)):
                        diffx = x[i] - x[i - 1]
                        diffy = y[i] - y[i - 1]
                        mdlx += diffx
                        mdly += diffy
                        matrix[mdlx, mdly] = 2.0

                dataframe_apf = pd.DataFrame.from_records(matrix)
                sns.heatmap(dataframe_apf, fmt="d", vmin=-1.0, vmax=2.0)
                if path_here is None:
                    plt.show()
                else:
                    plt.savefig("{}/trajectory_{}.png".format(path_here, tra_idx), dpi=500)
                plt.close()



if __name__ == '__main__':
    logger = logging.getLogger("LoadTrajectories")
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    logger.info("Starting script")

    a = PrintTrajectories(log=logger)
    a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/test_b/")
    a.print_paths(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/test_b/", name="test_b_trajectories", apf=True)
    # a.print_paths(apf=True)
