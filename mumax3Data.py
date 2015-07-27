#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
import numpy.fft as fft

from ovfFile import OvfFile


class Mumax3Data:

    m_eps = 1e-6

    _points = None  #Number of points in one frame
    _coordinates = None

    _M_avg = None


    def _do_cart2cyl_for_M(self):
        Mcart = self.M

        Mcyl = np.zeros_like(Mcart)

        Mcyl[:,:,2] = Mcart[:,:,2]

        for Mcart_f, Mcyl_f in zip(Mcart, Mcyl):
            for mcart, mcyl in zip(Mcart_f, Mcyl_f):
                #print("cart:", mcart)
                mcyl[0] = np.sqrt(mcart[0]**2 + mcart[1]**2)
                mcyl[1] = np.arctan2(mcart[0], mcart[1])
                #print("cyl", mcyl)

        return Mcyl

    def _load_frame_from_csv(self, filename):

        m_raw = np.genfromtxt(filename, dtype=float, delimiter=',')

        a,b = m_raw.shape
        assert(a == 3*b)

        MX = np.reshape(m_raw[0:b, :], -1)
        MY = np.reshape(m_raw[b:2*b, :], -1)
        MZ = np.reshape(m_raw[2*b:3*b, :], -1)

        if self.points is None:
            # Here we do not know the number of non-zero elements
            M = []
            coordinates = []

            x = np.arange(0,b)

            X, Y = np.meshgrid(x,x, sparse=False)
            X = np.reshape(X, -1)
            Y = np.reshape(Y, -1)

            for mx, my, mz, x, y in zip(MX, MY, MZ, X, Y):
                abs_m = mx*mx + my*my + mz*mz
                if abs(abs_m - 1) < self.m_eps:
                    M.append(np.array([mx,my,mz]))
                    coordinates.append(np.array([x,y]))

            M = np.array(M)
            coordinates = np.array(coordinates)

            self.points, _ = M.shape
            self.coordinates = coordinates

        else:
            M = np.zeros((self.points, 3))
            n = 0
            for mx, my, mz in zip(MX, MY, MZ):
                abs_m = mx*mx + my*my + mz*mz
                if abs(abs_m - 1) < self.m_eps:
                    M[n,:] = np.array([mx, my, mz])
                    n+=1

        return M

    def _set_non_zero_coordinates(self, frame):

        xnodes = frame.headers['xnodes']
        ynodes = frame.headers['ynodes']

        x = np.arange(0,xnodes, dtype=int)
        y = np.arange(0,ynodes, dtype=int)

        X, Y = np.meshgrid(x, y, sparse=False)
        X = np.reshape(X, -1)
        Y = np.reshape(Y, -1)

        layer = frame.array[:,:,0].reshape(-1,3)

        coordinates = []

        for m, x, y in zip(layer, X, Y):
            abs_m = np.sqrt(m.dot(m))
            if np.abs(abs_m - 1) < self.m_eps:
                coordinates.append(np.array([x,y]))

        self._coordinates = np.array(coordinates)
        self._points = self._coordinates.shape[0]


    def _load_frame_from_ovf(self, frame):

        if self._coordinates is None:
            self._set_non_zero_coordinates(frame)

        znodes = int(frame.headers['znodes'])

        M = np.zeros((znodes, self._points, 3), dtype=float)
        for z in range(0, znodes):
            layer = frame.array[:,:,z]
            for n, m  in zip(self._coordinates, M[z]):
                m[...] = layer[n[0],n[1]]

        time = frame.time

        return (M, time)

    def _load_all_frames(self, dir, n_min, n_max, format='ovf'):

        filename = os.path.join(dir, 'm{:06d}.ovf'.format(n_min))
        frame = OvfFile(filename)

        self._set_non_zero_coordinates(frame)

        znodes = int(frame.headers['znodes'])

        M = np.zeros((n_max-n_min, znodes, self._points, 3), dtype=float)
        T = np.zeros(n_max-n_min, dtype=float)
        print(M.shape)

        for n in range(n_min, n_max):
            filename = os.path.join(dir, 'm{:06d}.ovf'.format(n))
            frame = OvfFile(filename)
            Mt, t = self._load_frame_from_ovf(frame)
            M[n - n_min] = Mt
            T[n - n_min] = t
            if n%50 == 0:
                print('File {filename} loaded'.format(filename=filename))

        self.M = M
        self.ticks = n_max - n_min

    @classmethod
    def load_from_dir(Cls, dir, n_min, n_max):
        data = Cls()
        data._load_all_frames(dir, n_min, n_max)
        data.Mcyl = data._do_cart2cyl_for_M()
        return data

    @classmethod
    def load_from_npz(Cls, filename):
        data = Cls()
        saved_data = np.load(filename)
        data.M = saved_data['M']
        data.ticks = int(saved_data['ticks'])
        data.points = int(saved_data['points'])
        data.coordinates = saved_data['coordinates']
        data.Mcyl = saved_data['Mcyl']
        return data

    def save_to_file(self,filename):
        np.savez(filename, M = self.M, ticks = self.ticks, points = self.points,
                coordinates = self.coordinates, Mcyl = self.Mcyl)

    @property
    def M_avg(self):
        if self._M_avg is None:
            self._M_avg = np.sum(self.M, axis=1)/self.points
        return self._M_avg

