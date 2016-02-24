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
import struct


def _write_to_file(f):

    __TEST_VALUE_4 = 1234567.0

    metadata = '''# OOMMF OVF 2.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: m
# meshtype: rectangular
# meshunit: m
# xmin: 0
# ymin: 0
# zmin: 0
# xmax: 1.28e-06
# ymax: 6.4e-07
# zmax: 5e-09
# valuedim: 3
# valuelabels: m_x m_y m_z
# valueunits: 1 1 1
# Desc: Total simulation time:  0  s
# xbase: 2.5e-09
# ybase: 2.5e-09
# zbase: 2.5e-09
# xnodes: 256
# ynodes: 128
# znodes: 1
# xstepsize: 5e-09
# ystepsize: 5e-09
# zstepsize: 5e-09
# End: Header
# Begin: Data Binary 4
'''

    f.write(metadata.encode('ascii'))

    f.write(struct.pack("<f",__TEST_VALUE_4))
    for i in range(1*256*128):
        f.write(struct.pack("<fff",1.0,0.0,0.0))

def main():
    filename = "test_m.ovf"
    with open(filename, 'wb') as f:
        _write_to_file(f)

if __name__=='__main__':
    main()

