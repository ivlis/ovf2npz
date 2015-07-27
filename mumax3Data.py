#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
import numpy.fft as fft


class Mumax3Data:

    m_eps = 1e-6

    points = None  #Number of points in one frame
    ticks = None   #Number of time frames

    _M_avg = None

    dt = 0.2e-9    #Time step  (this should be loaded)

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

    def _load_all_frames(self, dir, n_min, n_max):

        filename = os.path.join(dir, 'm{:06d}.csv'.format(n_min))
        Mt = self._load_frame_from_csv(filename)

        M = np.zeros((n_max-n_min, self.points, 3))
        M[0,:,:] = Mt

        for n in range(n_min+1, n_max):
            filename = os.path.join(dir, 'm{:06d}.csv'.format(n))
            Mt = self._load_frame_from_csv(filename)
            M[n - n_min, :, :] = Mt
            if n%50 == 0:
                print('File {filename} loaded'.format(filename=filename))

        self.M = M
        self.ticks = n_max - n_min

    @classmethod
    def load_from_dir(Cls, dir, n_min, n_max):
        data = MumaxData()
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

