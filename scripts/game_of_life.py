#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import random   
import time
from PIL import Image
random.seed()


class GOL:
    def __init__(self):
        self.active = list()
        self.size = 60
        self.consideration = list()
        self.next_iter = list()
        self.neighbours = list()
        self.variation = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1) ]
        self.env = np.random.randint(low = 0, high = 2, size = (self.size, self.size))
    def init_env(self):
        self.active.clear()
        self.env = np.random.randint(low =0, high = 2, size = (self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                if self.env[i,j] == 1:
                    self.active.append((i,j))
        self.populate_neighbours(self.active)
    def reset_env(self):
        self.env = np.zeros((self.size, self.size)).astype(int)
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
                print(self.env[i,j], end = "")
            print()
        return
    def show_env(self):
        plt.clf()
        plt.imshow(game.env, cmap=plt.cm.gray)
        plt.draw()
        plt.show(block = False)
        plt.pause(0.1)
        return


if __name__ == "__main__":
    game = GOL()
    game.init_env()
    for i in range(200):        
        print("ITER "+str(i) + "\n\n")
        # for i in range(game.size):
        #     print(str(i), end="")
        # print()
        game.update_environment(game.active)
        game.show_env()
        print("Active: " +str(len(game.active)) + "\t Neighbourhood:"+ str(len(game.neighbours)))
        game.compute_next_live(game.active, game.neighbours)
        #print("Active: " +str(len(game.active)) + "\t Neighbourhood:"+ str(len(game.neighbours)))
        game.update_vars()
        #print("Active: " +str(len(game.active)) + "\t Neighbourhood:"+ str(len(game.neighbours)))
        
        time.sleep(0.1)
