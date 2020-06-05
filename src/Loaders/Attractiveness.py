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
import itertools


class ForcedAttractiveness(object):
    def __init__(self, log):
        # amenity
        # natural
        # office
        # shop
        # sport
        # building
        self.v = list(set(itertools.permutations([1, 1, 1, 1, 50, 100])))
        log.info("Testing {} permutation of attraction".format(len(self.v)))
