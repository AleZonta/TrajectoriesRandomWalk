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
import glob
import pickle

from tqdm import tqdm

from src.Analysis.Utils.funcs import sorted_nicely


class DataLoader(object):
    def __init__(self, log):
        self._log = log
        self._paths_generated = []
        self._tra_generated = []
        self._real_tra_generated = []

    def read_data(self, path):
        # read all the folders
        folders = sorted_nicely(glob.glob("{}*/".format(path)))
        for fold in tqdm(folders, desc="reading folders"):
            read_file = "{}/paths_0.pickle".format(fold)
            data = pickle.load(open(read_file, 'rb'))
            self._paths_generated.append(data)

            read_file = "{}/real_tra_0.pickle".format(fold)
            data = pickle.load(open(read_file, 'rb'))
            self._tra_generated.append(data)

            read_file = "{}/tra_0.pickle".format(fold)
            data = pickle.load(open(read_file, 'rb'))
            self._real_tra_generated.append(data)
        self._log.info("Data Read")