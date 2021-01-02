# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 00:57:21 2020

@author: benja
"""

import os
from os.path import join, isfile

def cleaner():
    files_list = [f for f in os.listdir() if isfile(join(f))]
    print (files_list)
    for f in files_list:
        if os.stat(f).st_size == 0:
            os.remove(f)
                
cleaner()