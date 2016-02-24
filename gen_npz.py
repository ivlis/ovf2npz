#!/usr/bin/env python3
# encoding: utf-8

import numpy as np

def main():

    array = np.zeros((10,20,3), dtype=float)
    array[:,:,0] =0.1
    array[:,:,1] =1.0
    array[:,:,2] =0.88
    array[9,19,2] = 102

    np.save("test_m.npy", array)


if __name__=='__main__':
    main()

