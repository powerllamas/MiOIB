# -*- coding: utf-8 -*-

class Instance(object):

    def __init__(self, filename):
        self.flow = []
        self.distance = []
        print "Loading file '{0}'...".format(filename)
        with open(filename) as f:
            self.nr_of_rows = int(f.readline())
            print "Instance size: {0}".format(self.nr_of_rows)
            f.readline()
            for i in xrange(self.nr_of_rows):
                row = f.readline().split()
                self.flow.append([float(x) for x in row])
            f.readline()
            for i in xrange(self.nr_of_rows):
                row = f.readline().split()
                self.distance.append([float(x) for x in row])
        print "File loaded!"

    def __len__(self):
        return self.nr_of_rows
