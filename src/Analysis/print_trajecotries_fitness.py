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
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm, trange

from src.Analysis.Utils.funcs import compute_direction
from src.Analysis.data_loader import DataLoader
from src.Helpers.Fitness.ValueGraphFitness import convert, MAX_FITNESS
from src.Settings.args import args
from src.Utils.Funcs import compute_fintess_trajectory


class AstarFitnessAnalyser(DataLoader):
    def __init__(self, log):
        super().__init__(log)

    def print_fitness_per_tra(self, name_to_save, path_to_save):
        # need to check from the same starting points with different behaviours
        # return all the tra same index
        df = pd.DataFrame(columns=['fitness', 'total_length', 'curliness', "f_d_to_p",
                                   "d_to_m_pt", "d_to_end_p", "direction",
                                   "no_overlapping"])

        for i in range(args.n_tra_generated):
            # make the trajectories readable
            current_analysed = []
            for j in range(len(self._paths_generated)):
                tra_points = self._paths_generated[j][i]

                current_analysed.append(tra_points)

            # get the fitness of all the trajectories
            fitness_trajectories = []
            behaviours = []
            for tra in tqdm(current_analysed, desc="computing fitness tra {}".format(i)):
                out, behaviour = compute_fintess_trajectory(tra_moved_so_far=tra)
                fitness_trajectories.append(out)
                behaviours.append(np.array(behaviour))

            # get more info from the trajectories generated
            values_of_same_elements = []
            for ii in trange(len(current_analysed), desc="computing overlapping tra {}".format(i)):
                first_tra = [[int(p.x), int(p.y)] for p in current_analysed[ii]]
                for j in range(ii + 1, len(current_analysed)):
                    second_tra = [[int(p.x), int(p.y)] for p in current_analysed[j]]
                    tot = [*first_tra, *second_tra]

                    equality = pd.DataFrame(np.array(tot).T).T.drop_duplicates(keep=False).values.shape[0] / len(
                        tot)
                    # s = min(len(first_tra), len(second_tra))
                    # count = np.count_nonzero(first_tra[:s] == second_tra[:s])
                    # number of similar value over s
                    # equality = 1 - (count / (s * 2))
                    values_of_same_elements.append(equality)
            average_distance = np.mean(np.array(values_of_same_elements))
            # 0 is exactly the same vectors
            # 1 is exactly different vectors
            average_converted_distance = convert(old_max=1, old_min=0, new_max=MAX_FITNESS, new_min=0,
                                                 old_value=average_distance)

            # need to force to go to four directions

            # I have starting point
            # I have ending points
            all_the_directions = [compute_direction(origin=tra[0], destination=tra[-1]) for tra in current_analysed]

            all_result_normal_general = np.mean(np.array(fitness_trajectories))
            all_result_behaviours_general = np.mean(np.array(behaviours), axis=0)
            single_direction_value = len(set(all_the_directions))

            self._log.info("Fitness current set {} of trajectories {} {} {} {}".format(i, all_result_normal_general,
                                                                                       all_result_behaviours_general,
                                                                                       single_direction_value,
                                                                                       average_converted_distance))
            df.loc[i] = [all_result_normal_general, all_result_behaviours_general[0],
                         all_result_behaviours_general[1] * 100,
                         all_result_behaviours_general[2], all_result_behaviours_general[3],
                         all_result_behaviours_general[4], single_direction_value * 100, average_converted_distance]
        df.to_hdf("{}/{}_save".format(path_to_save, name_to_save), key='data', mode='w')
        self._log.info("Data Saved!")

    def print_graphs(self, path_to_read, name_to_read):
        df = pd.read_hdf("{}/{}_save".format(path_to_read, name_to_read))
        sns.boxplot(data=df)
        sns.despine(offset=10, trim=True)
        # chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
        plt.savefig("{}/graph_{}.png".format(path_to_read, name_to_read), dpi=500)
        plt.close()
        # plt.show()


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

    a = AstarFitnessAnalyser(log=logger)
    a.print_graphs(name_to_read="random_walk_standard", path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")


    a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_standard_no_visited/")
    a.print_fitness_per_tra(name_to_save="random_walk_standard_no_visited",
                            path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    a.print_graphs(name_to_read="random_walk_standard_no_visited", path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")

    a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_standard_weighted/")
    a.print_fitness_per_tra(name_to_save="random_walk_standard_weighted",
                            path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    a.print_graphs(name_to_read="random_walk_standard_weighted",
                   path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")

    a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_weighted_no_visited/")
    a.print_fitness_per_tra(name_to_save="random_walk_weighted_no_visited",
                            path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    a.print_graphs(name_to_read="random_walk_weighted_no_visited",
                   path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")

