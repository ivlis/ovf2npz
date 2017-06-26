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


import numpy as np

import argparse
import struct


def _write_to_file(f, array):

    __TEST_VALUE_4 = 1234567.0

    x,y,_ = array.shape

    metadata = '''# OOMMF OVF 2.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: m
# meshtype: rectangular
# meshunit: m
# valuedim: 3
# xnodes: {xnodes}
# ynodes: {ynodes}
# znodes: 1
# End: Header
# Begin: Data Binary 4
'''.format(xnodes = x, ynodes = y)

    f.write(metadata.encode('ascii'))

    f.write(struct.pack("<f",__TEST_VALUE_4))
    array = np.swapaxes(array,0,1)
    flattend_array = np.ravel(array,order='C')
    f.write(struct.pack("<"+"fff"*x*y,*flattend_array))

def nparray2ovf(filename, array):
    with open(filename, 'wb') as f:
        _write_to_file(f, array)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("npz", help="npz filename")
    parser.add_argument("ovf", help = "ovf filename")
    args = parser.parse_args()

    array = np.load(args.npz)
    filename = args.ovf
    nparray2ovf(filename, array)


if __name__=='__main__':
    main()
