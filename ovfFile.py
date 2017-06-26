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
    def __create_decoder(f, array_size):
        """Creates appropriate decoding object

        :f: file object stopped right before data
        :returns: (struct decoder, chunk size)

        We currently support only 4 byte floats

        """

        __TEST_VALUE_4 = 1234567.0

        test_value = f.read(4)

        pattern = 'fff'*array_size

        if struct.unpack('<f', test_value)[0] == __TEST_VALUE_4:
            return (struct.Struct('<'+pattern), 4*3*array_size)
        elif  struct.unpack('>f', test_value)[0] == __TEST_VALUE_4:
            return (struct.Struct('>'+pattern), 4*3*array_size)
        else:
            raise Exception("Unsupported format")

    def __parse_file(self, filename, cached_dc_and_chunksize = None):
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

            znodes = int(headers['znodes'])
            ynodes = int(headers['ynodes'])
            xnodes = int(headers['xnodes'])

            array_size = znodes*ynodes*xnodes

            if cached_dc_and_chunksize is None:
                dc, chunksize = self.__create_decoder(f, array_size)
            else:
                dc, chunksize = cached_dc_and_chunksize

            flat_array = np.array(dc.unpack(f.read(chunksize))).reshape((znodes, ynodes, xnodes, 3))
            outArray = np.swapaxes(flat_array, 0,2)
            # outArray = np.swapaxes(outArray, 0,1)


        self._array = outArray
        self._headers = headers
        self._time = time

        self._dc_and_chunksize = (dc, chunksize)

    @property
    def array(self):
        return self._array

    @property
    def time(self):
        return self._time

    @property
    def headers(self):
        return self._headers

    @property
    def dc_and_chunksize(self):
        return self._dc_and_chunksize

    def __init__(self, filename, cached_dc_and_chunksize = None):
        self.__parse_file(filename, cached_dc_and_chunksize)
