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
import logging
import os

import numpy as np
from tqdm import tqdm
from src.Analysis.data_loader import DataLoader
import folium


class PrintTrajectories(DataLoader):
    def __init__(self, log):
        super().__init__(log)

    def print_paths(self, path=None, name=None):

        if path is not None:
            path = "{}/{}/".format(path, name)
            os.mkdir(path)

        for idx, attraction_variant in enumerate(self._tra_generated):
            if path is not None:
                path_here = "{}/set_attraction_{}/".format(path, idx)
                os.mkdir(path_here)
            else:
                path_here = None
            for tra_idx, tra in tqdm(enumerate(attraction_variant),
                                     desc="printing trajectories variant {}".format(idx)):
                x = []
                y = []
                coordinates = []
                for points in tra:
                    x.append(float(points.x))
                    y.append(float(points.y))
                    coordinates.append([float(points.y), float(points.x)])

                m = folium.Map(location=[np.mean(np.array(y)), np.mean(np.array(x))], zoom_start=13)

                my_PolyLine = folium.PolyLine(locations=coordinates, weight=5)
                m.add_children(my_PolyLine)
                m.save("{}/real_map_{}.html".format(path_here, tra_idx))

                # gmap3.scatter(y, x, '# FF0000',
                #               size=2, marker=False)
                #
                # gmap3.plot(y, x,
                #            'cornflowerblue', edge_width=2.5)
                #
                # gmap3.draw("{}/test_map_{}.html".format(path_here, tra_idx))


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
    a.read_data(path="/Users/alessandrozonta/PycharmProjects/astar/output/test_astar/")
    a.print_paths(path="/Users/alessandrozonta/PycharmProjects/astar/output/", name="test_new_pictures")
    # a.print_paths(apf=True)
