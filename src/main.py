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
import sys

from src.Experiment.Controller import Controller
from src.Loaders.Attractiveness import ForcedAttractiveness
from src.Settings.args import args

if __name__ == '__main__':
    # create console handler
    logger = logging.getLogger(args.name_exp)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    path = "{}/{}/".format(args.output_path, args.name_exp)
    try:
        os.mkdir(path)
    except OSError:
        logger.error("Experiment already present")
        sys.exit()
    args.output_path = path

    # create file handler
    fh = logging.FileHandler("{}/{}.log".format(args.output_path, args.name_exp))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.info("Starting experiment")
    apf_path = args.data_path + args.apf_name

    logger.info("-------------------------- loading data")
    a = Controller(path_apf=apf_path, name_exp=args.name_exp, log=logger)
    d = ForcedAttractiveness(log=logger)
    logger.info("-------------------------- data loaded")
    name_counter = 0
    for vector in d.v:
        logger.info("Testing {} vector".format(vector))
        name = "generate_tra_per_force"
        path = "{}/{}_version_{}/".format(args.output_path, name, name_counter)
        args.name_exp = "{}_version_{}".format(name, name_counter)
        try:
            os.mkdir(path)
        except OSError:
            logger.error("Creation of the directory %s failed" % path)
            logger.error("Folder already present")
        else:
            logger.info("Successfully created the directory %s " % path)
            a.set_vector_data(vector_data=vector)
            a.initialise_individual_and_run(save_path=path, how_many=args.n_tra_generated, debug=True)

        name_counter += 1
