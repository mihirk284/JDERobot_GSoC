#!/usr/bin/env python3

import json
import numpy as np
from matplotlib import pyplot as plt
import random   
import time
random.seed()


class GOL:
    def __init__(self, env_size=60):
        self.active = list()
        self.size = env_size
        self.consideration = list()
        self.next_iter = list()
        self.neighbours = list()
        self.variation = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1) ]
        self.env = np.zeros((self.size, self.size)).astype(int)
        self.BEACON = list()
        self.BLOCK = list()
        self.GLIDER = list()
        self.LWSS = list()
        self.BLINKER = list()
        self.TUB = list()
        self.load_shapes()
    
    def load_shapes(self):
        
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

    def init_env(self, tuple_list = None):
        self.active.clear()
        #print(tuple_list)        
        if (tuple_list == None):
            self.env = np.random.randint(low =0, high = 2, size = (self.size, self.size))
            for i in range(self.size):
                for j in range(self.size):
                    if self.env[i,j] == 1:
                        self.active.append((i,j))
        else:
            for i in tuple_list:
                self.env[i[0], i[1]] = 1
                self.active.append(i)        
        self.populate_neighbours(self.active)
    def reset_env(self):
        self.env = np.zeros((self.size, self.size)).astype(int)
        self.active = list()
    def count_live_neighbours(self, current , active_list):
        self.live_count = 0
        for dv in self.variation:
            if (current[0]+dv[0], current[1]+dv[1]) in active_list:
                self.live_count+=1
        return self.live_count
    def populate_neighbours(self,active_list):
        self.neighbours.clear()
        for a in active_list:
            for v in self.variation:
                if not ((a[0]+v[0], a[1]+v[1]) in active_list):
                    self.neighbours.append((a[0]+v[0], a[1]+v[1]))
        self.neighbours = self.neighbours + active_list
        self.neighbours = list(set(self.neighbours))
        self.neighbours = [cell for cell in self.neighbours if self.check_valid(cell)]
    def compute_next_live(self,active_list, neighbours):
        self.next_iter.clear()
        for c in neighbours:
            n_count = self.count_live_neighbours(c, active_list)
            #print("Neighbours:" +str(n_count))
            if (c in active_list) and n_count in [2,3]:
                self.next_iter.append(c)
            if ((not c in active_list) and n_count == 3):
                self.next_iter.append(c)
    def update_environment(self,active):
        self.reset_env()
        self.active = active
        for iter in active:
            self.env[iter[0], iter[1]] = 1
    def check_valid(self, cell):
        return (cell[0] in range(self.size) and cell[1] in range(self.size))
    def update_vars(self):
        self.active.clear()
        self.active = self.active + self.next_iter
        self.populate_neighbours(self.active)
        self.next_iter.clear()
    def print_env(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.env[i,j], end="")
            print()
        return
    def show_env(self):
        plt.clf()
        plt.imshow(self.env, cmap=plt.cm.gray)
        plt.draw()
        plt.show(block = False)
        plt.pause(0.02)
        return
    def add_object(self, occupied_list=None, x_ref =0 , y_ref =0):
        if occupied_list is not None:
            for i in occupied_list:
                self.env[x_ref+i[0], y_ref+ i[1]] = 1
                self.active.append((x_ref+i[0], y_ref + i[1]))
    def get_state(self):
        return self.env
    def update(self):
        self.populate_neighbours(self.active)
        self.compute_next_live(self.active, self.neighbours)
        self.update_vars()
        self.update_environment(self.active)