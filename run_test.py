#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: run_test.py


import os, sys
import glob
import subprocess
import re

EXEC = './test'
THRESHOLD = 0.8

'''def good_size(x_test, x_truth):
    ratio = x_test * 1.0 / x_truth
    if ratio > 1:
        ratio = 1.0 / ratio
    return ratio > THRESHOLD
'''
def test_final_size(image_globs):
    print "Testing with {}".format(image_globs)
    images = sorted(glob.glob(image_globs))
    cmd = [EXEC] + images
    outputs = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    outputs = outputs.split('\n')
    print '\n'.join(outputs)
    #sys.exit(1)

if __name__ == '__main__':
    test_final_size('example-data/test_m/*')
    print "Tests Passed"
