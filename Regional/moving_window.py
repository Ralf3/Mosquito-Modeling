#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 12:20:152017

@author: ralf
"""

""" datenanlyse Antje"""

import numpy as np
from scipy.ndimage.filters import convolve
import matplotlib.pyplot as plt
import argparse 
import sys
import os
sys.path.append(os.environ['SAMT2MASTER']+"/src")
import grid as samt2


def convert(matrix,N=7):
    """ moving windo using colvolve:
        input matrix and N=7
        output conv
    """
    w=np.ones((N,N))
    w/=N**2
    out=convolve(matrix,w,mode='constant',cval=-2)
    out[matrix==-1]=-1
    return out

def main():
    parser = argparse.ArgumentParser(description='Moving Window')
    parser.add_argument('-f', help='csv-data filename',required=True)
    parser.add_argument('-N', help='size of radius in csize')
    args = parser.parse_args()
    grid=args.f
    gi=samt2.grid()
    gi.read_ascii(grid)
    matrix=gi.get_matc() # read it
    matrix[matrix==gi.get_nodata]=0.0 # you may to adapt this
    if(args.N):
        N=int(args.N)
    else:
        N=7
    out=convert(matrix,N=N)
    # store the convolution as ascii grid
    s=args.f
    s=grid.split('.')
    filename=s[0] + '_' + str(N) + '.asc'
    out[out<0]=0
    out[gi.get_matp()==gi.get_nodata()]=gi.get_nodata()
    gi.set_mat(out)
    gi.show()
    gi.write_ascii(filename)
    # np.save(filename,out,allow_pickle=False)

main()
