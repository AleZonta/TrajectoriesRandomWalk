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
import random


def random_wrapper_uniform(lower_bound, upper_bound):
    return random.uniform(lower_bound, upper_bound)


def random_wrapper_normal(mean, std):
    return np.random.normal(mean, std)


def random_wrapper_lognorm(mean, std):
    return np.random.lognormal(mean, std)


def random_wrapper_randint(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)


def random_wrapper_normalvariate(mean, std):
    return np.random.normal(mean, std)
    # return random.normalvariate(mean, std)


def random_wrapper_normalvariate(mean, std, elements):
    return np.random.normal(mean, std, size=elements)


def random_wrapper_sample(population, k):
    return random.sample(population, k)
