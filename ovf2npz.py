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


def main():
    ovffile = OvfFile("m000020.ovf")


if __name__=='__main__':
    main()

