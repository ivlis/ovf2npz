#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
ovf2npz.py
Copyright (C) 2015  Ivan Lisenkov

ivan.lisenkov@phystech.edu

Institute of Radioengineering and Electronics of RAS
Moscow, Russia

AND

Department of Physics
Oakland University
Rochester, Michigan, USA

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""


import os
import sys

from ovfFile import OvfFile
from mumax3Data import Mumax3Data

import argparse



def main():

    # This should be reformulated as a test
    ovffile = OvfFile("test_m.ovf")
    print(ovffile.array[:,:,0])
    exit(-1)

    parser = argparse.ArgumentParser()
    parser.add_argument("data_directory", help="directory with mumax3 output files")
    parser.add_argument("start_frame", help = "number of frame to start with")
    parser.add_argument("stop_frame", help = "number of frame to stop")
    args = parser.parse_args()

    dir = args.data_directory

    if dir[-1] == '/':
        dir = dir[:-1]


    min_t = int(args.start_frame)
    max_t = int(args.stop_frame)
    data = Mumax3Data.load_from_dir(dir, min_t, max_t)

    basename = os.path.basename(dir)[:-4] ## Dir name with .out removed

    data.save_to_file('{basename}_{min_t}-{max_t}.npz'.format(basename = basename, min_t = min_t,
        max_t = max_t))


if __name__=='__main__':
    main()

