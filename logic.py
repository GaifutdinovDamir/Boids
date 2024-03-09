import pygame
import os
import numpy as np
from random import randint 

HEIGHT, WIDTH = 500, 500
MARGIN = 100

TOPMARGIN = MARGIN
BOTTOMMARGIN = HEIGHT - MARGIN
LEFTMARGIN = MARGIN
RIGHTMARGIN = WIDTH - MARGIN

#START_LINE = pygame.font.SysFont('comic_sans', 40)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 120)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

SIZE = 400

TURNFACTOR = 0.1
PREDATORTURN = 0.2
VISUALRANGE = 40
PROTECTEDRANGE = 8
PREDATORRANGE = 60

CENTERING = 0.0005
MATCHING = 0.026
AVOIDMENT = 0.05
BIASVAL = 0.001

MAXSPEED = 8.
MINSPEED = 5.

class Boid():
    def __init__(self, pos = np.array([0, 0]), vel = np.array([0, 0])):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
    
#class Hunter(Boid):
    
def generate_random_boids(size):
    boids = []
    for i in range(size):
        boids.append(Boid())
        boids[i].pos, boids[i].vel = ([np.random.uniform(LEFTMARGIN, RIGHTMARGIN, 1)[0], np.random.uniform(TOPMARGIN, BOTTOMMARGIN, 1)[0]],
                        np.random.uniform(MINSPEED, MAXSPEED, 2))
    return boids

class FLock():
    def __init__(self, boids, n):
        self.bx = np.array([boid.pos[0] for boid in boids])
        self.by = np.array([boid.pos[1] for boid in boids])
        self.bvx = np.array([boid.vel[0] for boid in boids])
        self.bvy = np.array([boid.vel[1] for boid in boids])

        self.distance_matrix = np.empty((n, n))
        self.nboids = n
    """
    def append_boid(self, Boid):
        np.append(self.arr, Boid)
        new_dist_matrix = np.empty((self.nboids + 1, self.nboids + 1))
        new_dist_matrix[:n, :n] = self.diistance_matix[:, :]
        new_dist_matrix[0:n, -1] =
    def delete_boid
    """
    def step(self, px, py):
        for i in range(self.nboids):
            self.distance_matrix[:][i] = (self.bx - self.bx[i]) ** 2 + (self.by - self.by[i]) ** 2
        #update velocity
        new_bvx = self.bvx[:]
        new_bvy = self.bvy[:]
        for i in range(self.nboids):
            #separation
            new_bvx[i] += (self.bx[i] - self.bx[self.distance_matrix[i][:] < PROTECTEDRANGE]).sum() * AVOIDMENT
            new_bvy[i] += (self.by[i] - self.by[self.distance_matrix[i][:] < PROTECTEDRANGE]).sum() * AVOIDMENT

            #centering 
            help_arr = (self.distance_matrix[i][:] > PROTECTEDRANGE) | (self.distance_matrix[i][:] < VISUALRANGE)
            new_bvx[i] += (self.bx[help_arr] - self.bx[i]).mean() * CENTERING
            new_bvy[i] += (self.by[help_arr] - self.by[i]).mean() * CENTERING

            #matching
            new_bvx[i] += (self.bvx[help_arr] - self.bvx[i]).mean() * MATCHING
            new_bvy[i] += (self.bvy[help_arr] - self.bvy[i]).mean() * MATCHING

        self.bvx[:] = new_bvx[:]
        self.bvy[:] = new_bvy[:]
        #margins
        self.bvy[self.by < TOPMARGIN] += TURNFACTOR
        self.bvy[self.by > BOTTOMMARGIN] -= TURNFACTOR
        self.bvx[self.bx < LEFTMARGIN] += TURNFACTOR
        self.bvx[self.bx > RIGHTMARGIN] -= TURNFACTOR

        #predator
        dist_to_pred = np.sqrt((px - self.bx) ** 2 + (py - self.by) ** 2)
        help_pred = dist_to_pred < PREDATORRANGE
        self.bvx[help_pred] += np.sign(self.bx - px)[help_pred] * PREDATORTURN
        self.bvy[help_pred] += np.sign(self.by - py)[help_pred] * PREDATORTURN

        #Bias
        self.bvx[:SIZE//2] = self.bvx[:SIZE//2] * (1 - BIASVAL) + BIASVAL
        self.bvx[SIZE//2:] = self.bvx[SIZE//2:] * (1 - BIASVAL) - BIASVAL

        #max min speed
        speed = self.bvx ** 2 + self.bvy ** 2
        self.bvx[speed > MAXSPEED ** 2] *=  MAXSPEED / speed[speed > MAXSPEED ** 2] 
        self.bvy[speed > MAXSPEED ** 2] *=  MAXSPEED / speed[speed > MAXSPEED ** 2]

        self.bvx[speed < MINSPEED ** 2] *=  MINSPEED / speed[speed < MINSPEED ** 2] 
        self.bvy[speed < MINSPEED ** 2] *=  MINSPEED / speed[speed < MINSPEED ** 2]

        #update position
        self.bx += self.bvx
        self.by += self.bvy

    def get_bx(self):
        return self.bx
    

    def get_by(self):
        return self.by



    

