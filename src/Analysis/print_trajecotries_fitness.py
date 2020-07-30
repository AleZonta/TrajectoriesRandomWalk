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
import copy
import glob
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import stats
from tqdm import tqdm, trange

from src.Analysis.Utils.funcs import compute_direction, sorted_nicely
from src.Analysis.data_loader import DataLoader
from src.Helpers.Fitness.ValueGraphFitness import convert, MAX_FITNESS
from src.Settings.args import args
from src.Utils.Funcs import compute_fintess_trajectory


class AstarFitnessAnalyser(DataLoader):
    def __init__(self, log):
        super().__init__(log)

    def print_fitness_per_tra(self, name_to_save, path_to_save):
        """
        Generate files with features value per trajectory generated to use for the paper graphs
        :param name_to_save:
        :param path_to_save:
        :return:
        """
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

    # get all the h5 files
    # find all the save files
    path_to_read = "/Users/alessandrozonta/Desktop/output_random_walk/"
    correct_files = glob.glob("{}/*_save".format(path_to_read))


    # different_fitness
    fit = ["fitness_no_visited_seed_pd0_", "fitness_no_visited_seed_pd1_", "fitness_no_visited_seed_pd01_", "fitness_no_visited_seed_pd012_",
           "fitness_no_visited_seed_pd2_", "fitness_no_visited_seed_pd12_", "fitness_no_visited_seed_pd02_", "fitness_no_visited_seed_standard_",
           "fitness_seed_pd0_", "fitness_seed_pd1_", "fitness_seed_pd01_", "fitness_seed_pd012_",
           "fitness_seed_pd2_", "fitness_seed_pd12_", "fitness_seed_pd02_", "fitness_seed_standard_",
           "standard_weighted_no_visited_seed_", "standard_weighted_seed_"]
    real_names = ["RWFBNV0", "RWFBNV1", "RWFBNV01", "RWFBNV012", "RWFBNV2", "RWFBNV12", "RWFBNV02", "RWFBNV",
                  "RWFB0", "RWFB1", "RWFB01", "RWFB012", "RWFB2", "RWFB12", "RWFB02", "RWFB",
                  "RWABNV", "RWAB"]
    rnm = dict(zip(fit, real_names))

    data_exp = []
    for f in fit:
        repetitions = [el for el in correct_files if f in el]
        logger.debug("{} - {}".format(f, len(repetitions)))
        for el in repetitions:
            correct_files.remove(el)
        dataframes = [pd.read_hdf(el) for el in repetitions]
        single_dataframe = pd.concat(dataframes)
        source = [rnm[f] for _ in range(single_dataframe.shape[0])]
        single_dataframe['source'] = source
        data_exp.append(single_dataframe)
    df = pd.concat(data_exp)

    min_dataframe = abs(df["fitness"].min())
    df["fitness"] = (df["fitness"] + min_dataframe) / (700 + min_dataframe)
    df["direction"] = df["direction"] / 800
    df["no_overlapping"] = df["no_overlapping"] / 200

    small_dataset = df[["direction", "fitness", "no_overlapping", "source"]]
    small_dataset.columns = ['Directions', 'Fitness', "No_Overlapping", "Source"]

    reshaped = small_dataset.melt(id_vars=['Source'], value_vars=['No_Overlapping', 'Fitness', 'Directions'])
    reshaped.columns = ['Versions', 'Measurements', "Score"]
    sns.boxplot(x="Measurements", y="Score", hue="Versions", data=reshaped, showfliers=False)
    sns.despine(offset=10, trim=True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig("{}/combined_graph_random_walk.pdf".format(path_to_read), bbox_inches='tight')
    # plt.show()
    plt.close()

    # for name in real_names:
    #     ax = sns.distplot(df[df["source"] == name]["total_length"], label=name, kde=False, rug=True)
    sns.boxplot(x="source", y="total_length", data=df, showfliers=False)
    # ax.set(xlabel='total length')
    plt.legend()
    sns.despine(offset=10, trim=True)
    plt.savefig("{}/total_length_random_walk.pdf".format(path_to_read))
    # plt.show()
    plt.close()

    to_check = ["fitness", "no_overlapping", "direction"]

    for c in to_check:
        for f in fit:
            here_list = copy.deepcopy(fit)
            here_list.remove(f)

            total = []
            # for el in here_list:
            total.append(stats.ks_2samp(df[df["source"] == "fitness_no_visited_seed_pd0_"][c], df[df["source"] == "fitness_no_visited_seed_pd1_"][c]).pvalue)
            logger.info(f)
            logger.info(total)
            logger.info(np.mean(np.array(total)))
            logger.info(np.std(np.array(total)))
            logger.info("---")

        logger.info("------------------------")



    #
    # path = "/Users/alessandrozonta/Desktop/output_random_walk/"
    # folders = sorted_nicely(glob.glob("{}*/".format(path)))
    #
    # for f in folders:
    #     name_folder = f.split("/")[-1]
    #
    #     a.read_data(path="{}/{}".format(path, name_folder))
    #     a.print_fitness_per_tra(name_to_save=name_folder,
    #                             path_to_save="{}".format(path))
    #
    # a.print_graphs(name_to_read="random_walk_standard", path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    #
    #
    # a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_standard_no_visited/")
    # a.print_fitness_per_tra(name_to_save="random_walk_standard_no_visited",
    #                         path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    # a.print_graphs(name_to_read="random_walk_standard_no_visited", path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    #
    # a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_standard_weighted/")
    # a.print_fitness_per_tra(name_to_save="random_walk_standard_weighted",
    #                         path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    # a.print_graphs(name_to_read="random_walk_standard_weighted",
    #                path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    #
    # a.read_data(path="/Users/alessandrozonta/PycharmProjects/random_walk/output/random_walk_weighted_no_visited/")
    # a.print_fitness_per_tra(name_to_save="random_walk_weighted_no_visited",
    #                         path_to_save="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    # a.print_graphs(name_to_read="random_walk_weighted_no_visited",
    #                path_to_read="/Users/alessandrozonta/PycharmProjects/random_walk/output/")
    #
