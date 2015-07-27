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
        Mcart = self._M

        Mcyl = np.zeros_like(Mcart)

        Mcyl[:,:,2] = Mcart[:,:,2]

        for Mcart_f, Mcyl_f in zip(Mcart, Mcyl):
            for mcart, mcyl in zip(Mcart_f, Mcyl_f):
                #print("cart:", mcart)
                mcyl[0] = np.sqrt(mcart[0]**2 + mcart[1]**2)
                mcyl[1] = np.arctan2(mcart[0], mcart[1])
                #print("cyl", mcyl)

        return Mcyl

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

    def _set_frame_metadata(self, frame):

        self._xnodes = int(frame.headers['xnodes'])
        self._ynodes = int(frame.headers['ynodes'])
        self._znodes = int(frame.headers['znodes'])

        self._xstepsize = int(frame.headers['xstepsize'])
        self._ystepsize = int(frame.headers['ystepsize'])
        self._zstepsize = int(frame.headers['zstepsize'])


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

        self._set_frame_metadata(frame)

        znodes = self._znodes

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

        self._M = M
        self._ticks = n_max - n_min
        self._T = T

    @classmethod
    def load_from_dir(Cls, dir, n_min, n_max):
        data = Cls()
        data._load_all_frames(dir, n_min, n_max)
        data._Mcyl = data._do_cart2cyl_for_M()
        return data

    @classmethod
    def load_from_npz(Cls, filename):
        data = Cls()
        saved_data = np.load(filename)
        data._M = saved_data['M']
        data._T = saved_data['T']
        data._coordinates = saved_data['coordinates']

        data.xnodes = int(saved_data['xnodes'])
        data.ynodes = int(saved_data['ynodes'])
        data.znodes = int(saved_data['znodes'])

        data.xstepsize = int(saved_data['xstepsize'])
        data.ystepsize = int(saved_data['ystepsize'])
        data.zstepsize = int(saved_data['zstepsize'])

        data._Mcyl = saved_data['Mcyl']
        return data

    def save_to_file(self,filename):
        np.savez(filename, 
                M = self._M, 
                T = self._T, 
                coordinates = self._coordinates,
                xnodes = self._xnodes,
                ynodes = self._ynodes,
                znodes = self._znodes,
                xstepsize = self._xstepsize,
                ystepsize = self._ystepsize,
                zstepsize = self._zstepsize,
                Mcyl = self._Mcyl)

    @property
    def M_avg(self):
        if self._M_avg is None:
            self._M_avg = np.sum(self.M, axis=1)/self.points
        return self._M_avg

