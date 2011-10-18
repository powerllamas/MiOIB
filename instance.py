# -*- coding: utf-8 -*-

class Instance(object):

    def __init__(self, filename = None, distance = [], flow = []):
        self.flow = []
        self.distance = []
        if filename == None:
            self.flow = flow
            self.distance = distance
            self.nr_of_rows = len(flow)
        else:
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

    def __len__(self):
        return self.nr_of_rows

