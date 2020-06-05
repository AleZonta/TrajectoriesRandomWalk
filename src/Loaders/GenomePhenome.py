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
import os

import csv
import json
import pickle
from pathlib import Path

import numpy as np

from src.Settings.args import args


class GenomeMeaning(object):
    """
    Class representing what every position in the genome means

    It loads all the tag and subtag used in the system and it loads also the location of all the objects
    in the map
    """

    def __init__(self, logger=None):
        self._log = logger
        self._types = None
        self.number_typologies = 0
        self.name_typologies = []
        self.name_and_details = {}
        self.name_and_position = None
        self.list_of_names_per_genome = []
        self.link_main_obj_and_small_objs = {}
        self._features = 0
        self.order_name_and_position = None
        self.method_mmap = False

    def load_data(self, test, performance=True):
        """
        Load location data

        All the csv present in the Data folder are loaded
        The file in Settings/Phenotype has to contain the sub tag accepted by the system
        The file contains also the name of the files that have to be in the Data folder
        If one file is missing, the system raises an Exception

        If there are different tag in the file that are not in the Phenotype file, the tag is changed into others

        :param test: if test is true, test files are loaded (with fewer elements)
        :return:
        """
        # loading coordinates
        phenotype_file = args.data_path + "/Phenotype"
        with open(phenotype_file, 'r') as f:
            self._types = json.load(f)
        if self._log is not None:
            self._log.info("Phenotype meaning loaded")

        self.number_typologies = len(self._types["Typology"])

        for el in self._types["Typology"]:
            for k in el.keys():
                self.name_typologies.append(k.lower())
                self.name_and_details.update(
                    {k.lower(): [x.lower() if x.lower() != "others" else "others_" + k.lower() for x in el[k]]})


        self._log.debug("Typology loaded {}".format(self.name_typologies))

        mmap_file = "{}/name_and_position.dat".format(args.data_path)
        if os.path.isfile(mmap_file):
            self._log.debug("mmap file exist, loading it")

            self.name_and_position = np.memmap(mmap_file, dtype='float32', mode='r', shape=(56, 938737, 2))

            with open('{}/order_on_mmap.pickle'.format(args.data_path), 'rb') as handle:
                self.order_name_and_position = pickle.load(handle)

            with open('{}/name_typology.pickle'.format(args.data_path), 'rb') as handle:
                self.name_typologies = pickle.load(handle)
            self.method_mmap = True
        else:
            self.name_and_position = {}
            for name in self.name_typologies:
                lowercase_name = name.lower()
                root = os.path.dirname(os.path.abspath(__file__))
                data_file = root.replace("Loaders", "") + "/Data/"
                if test:
                    name_file = data_file + lowercase_name + "_test.csv"
                else:
                    name_file = data_file + lowercase_name + ".csv"
                my_file = Path(name_file)
                if my_file.is_file():

                    list_word_accepted = self.name_and_details[lowercase_name]
                    list_word_accepted_fixed = []
                    for word in list_word_accepted:
                        if word == "others":
                            word = "others_" + name
                        list_word_accepted_fixed.append(word)
                        self.link_main_obj_and_small_objs.update({word: name})
                    self.list_of_names_per_genome.extend(list_word_accepted_fixed)

                    # file exist
                    with open(name_file) as csvfile:
                        reader = csv.DictReader(csvfile)
                        dic = {}

                        for row in reader:
                            name_element = row["names"].lower()

                            if name_element in list_word_accepted:
                                okay_id = name_element
                            else:
                                okay_id = "others_" + name

                            if row["x"] != "":
                                dic.setdefault(okay_id, []).append((float(row["x"]), float(row["y"])))

                        self.name_and_position.update({lowercase_name: dic})
                else:
                    self._log.debug("File {} not present in folder. Please provide it".format(name_file))
                    raise ValueError("File {} not present in folder. Please provide it".format(name_file))

        self._log.info("Coordinates loaded!")
        self._log = None

        if performance:
            self._types = None
            self.name_and_details = None
