#!/usr/bin/env python3

import json
import numpy as np
from matplotlib import pyplot as plt
import random   
import time
from game_of_life import GOL
import unittest
random.seed()


class TestCgolMethods(unittest.TestCase):
    def setUp(self):
        self.g = GOL()
        self.testgrid = np.zeros((self.g.size, self.g.size)).astype(int)
        self.BEACON = list()
        self.BLOCK = list()
        self.GLIDER = list()
        self.LWSS = list()
        self.BLINKER = list()
        self.TUB = list()
        self.BLINKERVAR = list()
        self.BEACONVAR = list()
        self.LWSSVAR = list()
        self.GLIDERVAR = list()
        f = open('patterns.json')
        data = json.load(f)
        f.close()
        for i in data['members']:
            if i['pattern'] == 'glider':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.GLIDER.append((k))
            if i['pattern'] == 'block':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.BLOCK.append((k))
            if i['pattern'] == 'beacon':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.BEACON.append((k))
            if i['pattern'] == 'lwss':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.LWSS.append((k))
            if i['pattern'] == 'blinker':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.BLINKER.append((k))
            if i['pattern'] == 'tub':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.TUB.append((k))
            if i['pattern'] == 'beaconvar':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.BEACONVAR.append((k))
            if i['pattern'] == 'blinkervar':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.BLINKERVAR.append((k))
            if i['pattern'] == 'glidervar':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.GLIDERVAR.append((k))
            if i['pattern'] == 'lwssvar':
                x = i['x']
                y = i['y']
                for k in zip(x,y):
                    self.LWSSVAR.append((k))
    
    
    def test_created_grid(self):
        np.testing.assert_array_equal(self.g.get_state(), np.zeros((self.g.size, self.g.size)))

    def test_pattern_placement(self):
        self.g.add_object(self.BEACON, 0, 0)
        self.g.add_object(self.BLOCK, 10, 10)
        self.testgrid = np.zeros((self.g.size, self.g.size)).astype(int)
        for i in self.BEACON:
            self.testgrid[i[0]+0,i[1]+0]= 1
        for i in self.BLOCK:
            self.testgrid[i[0]+10,i[1]+10]= 1
        np.testing.assert_array_equal(self.g.get_state(), self.testgrid)

    def test_still_life(self):
        self.g.reset_env()
        self.g.add_object(self.BLOCK, 0, 0)
        self.g.add_object(self.TUB, 6, 12)
        self.g.update()
        self.testgrid = np.zeros((self.g.size, self.g.size))
        for i in self.BLOCK:
            self.testgrid[i[0]+0,i[1]+0]= 1
        for i in self.TUB:
            self.testgrid[i[0]+6,i[1]+12]= 1
        np.testing.assert_array_equal(self.g.get_state(), self.testgrid)
    
    def test_oscillators(self):
        self.g.reset_env()
        self.g.add_object(self.BLINKER, 0, 0)
        self.g.add_object(self.BEACON, 6, 12)
        self.g.update()
        self.testgrid = np.zeros((self.g.size, self.g.size))
        for i in self.BLINKERVAR:
            self.testgrid[i[0]+0,i[1]+0]= 1
        for i in self.BEACONVAR:
            self.testgrid[i[0]+6,i[1]+12]= 1
        np.testing.assert_array_equal(self.g.get_state(), self.testgrid)
    
    def test_spaceships(self):
        self.g.add_object(self.GLIDER, 4, 4)
        self.g.add_object(self.LWSS, 12, 5)
        self.g.update()
        self.testgrid = np.zeros((self.g.size, self.g.size))
        for i in self.GLIDERVAR:
            self.testgrid[i[0]+4,i[1]+4]= 1
        for i in self.LWSSVAR:
            self.testgrid[i[0]+12,i[1]+5]= 1
        np.testing.assert_array_equal(self.g.get_state(), self.testgrid)

if __name__ == '__main__':
    unittest.main()