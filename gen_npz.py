#!/usr/bin/env python3
# encoding: utf-8

import numpy as np

def main():

    array = np.zeros((6,4,3,3), dtype=float)
    array[:,:,0,0] = 1
    array[:,:,0,1] = 2
    array[:,:,0,2] = 3

    array[:,:,1,0] = 4
    array[:,:,1,1] = 5
    array[:,:,1,2] = 6

    array[0,2,2,2] = 10

    np.save("test_m3d.npy", array)


if __name__=='__main__':
    main()
