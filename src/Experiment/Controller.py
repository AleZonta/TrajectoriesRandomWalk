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
import multiprocessing
import pickle
from joblib import Parallel, delayed
from src.Helpers.Division.ComputeDivision import SubMatrix
from src.Individual.GenerativeIndividual import TrajectoryGeneration
from src.Loaders.GenomePhenome import GenomeMeaning
from src.Loaders.LoadAPF import LoadAPF
from src.Loaders.PlacesOnRoute import FindPlacesOnRoutes
from src.Settings.args import args


def worker_job_lib(individual, idx, random_seed):
    """
    Multiprocessing function that creates trajectories
    :param individual: current object that generates
    :param idx: index of the starting point
    :param random_seed: random seed
    :return: trajectories generated
    """
    distances, tra, real_tra, path = individual.create_trajectory(random_seed=random_seed, idx=idx)
    return (distances, tra, real_tra, path)


def save_data(vector_data, save_path, name, version):
    """
    Function that saves the data generated to disk
    :param vector_data: data to save
    :param save_path: path where to save the data
    :param name: name of the file to save
    :param version: version of the file to save
    :return:
    """
    all_real_points = []
    for el in vector_data:
        real_points = []
        for point in el:
            real_points.append(point.to_real_point())
        all_real_points.append(real_points)
    tra_path_real = "{}/{}_{}.pickle".format(save_path, name, version)
    pickle.dump(all_real_points, open(tra_path_real, 'wb'))


class Controller(object):
    def __init__(self, path_apf, name_exp, log):
        self._path_apf = path_apf
        self._name_exp = name_exp
        self._logger = log

        # need to load the controller from file saved -> path -> name I already know
        # decide which generation to use -> last? (0) or something before? (-1,....,-N)
        # load the controller and assign it to the generator
        # random position and taac, generate tra and save it
        self._list_genome = None

        self._loader_apf = LoadAPF(path=self._path_apf, logger=self._logger)
        self._loader_apf.load_apf_only_routing_system()
        self._loader_apf.match_index_with_coordinates()
        self._loader_genome_meaning = GenomeMeaning(logger=self._logger)
        self._loader_genome_meaning.load_data(test=False)

        self._sub_matrix = SubMatrix(log=self._logger,
                                     list_points=self._loader_genome_meaning.name_typologies,
                                     values_matrix=(self._loader_apf.x_values, self._loader_apf.y_values))
        self._sub_matrix.divide_into_cells()

        self._pre_loaded_points = FindPlacesOnRoutes(logger=self._logger)
        self._pre_loaded_points.load_preloaded_position()

    def set_vector_data(self, vector_data):
        """
        Read data from file and load the controller
        :param vector_data:
        :return:
        """
        self._list_genome = vector_data

    def initialise_individual_and_run(self, save_path, how_many, version="0", debug=False, random_seed=42):
        """
        Initialise the generator, run it using all the processors in the cpu
        save the results on disk
        :param save_path: where to save the data generated
        :param how_many: how many trajectories to generate
        :param version: version of the experiment
        :param debug: True if debug in single core is necessary, False multiprocessing is on
        :param random_seed: random seed
        :return:
        """
        individual = TrajectoryGeneration(
                                          genotype=self._list_genome,
                                          values_matrix=(self._loader_apf.x_values, self._loader_apf.y_values),
                                          apf=self._loader_apf.apf,
                                          pre_matrix=self._sub_matrix,
                                          type_of_generator=args.type_random_walk,
                                          pre_loaded_points=self._pre_loaded_points,
                                          total_distance_to_travel=args.total_distance_to_travel)

        self._logger.debug("Generating Trajectories")
        results = []
        number_of_processes = multiprocessing.cpu_count()
        if how_many < number_of_processes:
            number_of_processes = how_many
        if debug:
            # serial execution
            number_of_processes = 1
        with Parallel(n_jobs=number_of_processes, verbose=30) as parallel:
            res = parallel(delayed(worker_job_lib)(individual, i, random_seed) for i in range(how_many))
            results.append(res)

        # distances, tra, real_tra, path, preloaded_points
        total_tra = []
        # total_vector_distances = []
        total_real_tra = []
        total_paths = []
        for trial in results[0]:
            total_tra.append(trial[1])
            # total_vector_distances.append(trial[0])
            total_real_tra.append(trial[2])
            total_paths.append(trial[3])

        save_data(vector_data=total_real_tra, save_path=save_path, name="real_tra", version=version)
        save_data(vector_data=total_tra, save_path=save_path, name="tra", version=version)
        save_data(vector_data=total_paths, save_path=save_path, name="paths", version=version)

        self._logger.debug("Trajectories generated")
