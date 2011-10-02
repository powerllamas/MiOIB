# -*- coding: utf-8 -*-

import sys

filename = sys.argv[1]

flow = []
distance = []

print "Loading file '{0}'...".format(filename)

with open(filename) as f:
    nr_of_rows = int(f.readline())
    print "Instance size: {0}".format(nr_of_rows)
    f.readline()
    for i in xrange(nr_of_rows):
        row = f.readline().split()
        flow.append(row)
    f.readline()
    for i in xrange(nr_of_rows):
        row = f.readline().split()
        distance.append(row)

print "File loaded!"
