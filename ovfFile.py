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

import struct

import numpy as np

class OvfFile:

    @staticmethod
    def __create_decoder(f):
        """Creates appropriate decoding object

        :f: file object stopped right before data
        :returns: (struct decoder, chunk size)

        We currently support only 4 byte floats

        """

        __TEST_VALUE_4 = 1234567.0

        test_value = f.read(4)

        if struct.unpack('<f', test_value)[0] == __TEST_VALUE_4:
            return (struct.Struct('<fff'), 4*3)
        elif  struct.unpack('>f', test_value)[0] == __TEST_VALUE_4:
            return (struct.Struct('>fff'), 4*3)
        else:
            raise Exception("Unsupported format")

    def __parse_file(self,filename):
        with open(filename, 'rb') as f:
            headers = {}
            capture_keys = ("xmin", "ymin", "zmin", "xmin", "ymin", "zmin", "xstepsize",
                    "ystepsize", "zstepsize", "xnodes", "ynodes", "znodes")

            a = ""
            while not "Begin: Data" in a:
                a = f.readline().strip().decode('ASCII')
                for key in capture_keys:
                    if key in a:
                        headers[key] = float(a.split()[2])

                if "Total simulation time" in a:
                    time = float(a.split(":")[-1].strip().split()[0].strip())

            dc, chunksize = self.__create_decoder(f)

            #Initialize array to be populated
            outArray = np.zeros((int(headers["xnodes"]),
                                 int(headers["ynodes"]),
                                 int(headers["znodes"]),
                                 3))

            for k in range(int(headers["znodes"])):
                   for j in range(int(headers["ynodes"])):
                       for i in range(int(headers["xnodes"])):
                           outArray[i,j,k,:] = dc.unpack(f.read(chunksize))

        self._array = outArray
        self._headers = headers

    @property
    def array(self):
        return self._array

    @property
    def headers(self):
        return self._headers

    def __init__(self, filename):
        self.__parse_file(filename)

