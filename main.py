import sys
import math
import time
import pygame
import json

class Vertex():
    def __init__(self, pos):
        # Store position of one Vertex
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

class Object():
    # 3D Object with a pivot, vertices and edges
    def __init__(self, cntr, verts, edgs, col=(255,255,255)):
        self.x = cntr[0]
        self.y = cntr[1]
        self.z = cntr[2]

        self.vertices = verts  # Store positions of vertexes in a list
        self.edges = edgs       # Uses index to represent edges

        # rotation of object by all 3 axis
        # in degrees
        self.rx = 0
        self.ry = 0
        self.rz = 0

        self.colour = col
    
    # draw a the object using 
    def draw3D(self, screen):
        points = []
        for vert in self.vertices:
            # Calculation of rotation about x
            Rx = ( vert.x+self.x, 
                  (vert.y+self.y)*math.cos(self.rx*math.pi/180) + (vert.z+self.z)*math.sin(self.rx*math.pi/180), 
                  (vert.y+self.y)*-math.sin(self.rx*math.pi/180) + (vert.z+self.z)*math.cos(self.rx*math.pi/180))

            # Calculation of rotation about y
            Ry = ((Rx[0])*math.cos(self.ry*math.pi/180) + (Rx[2])*-math.sin(self.ry*math.pi/180),
                   Rx[1], 
                  (Rx[0])*math.sin(self.ry*math.pi/180) + (Rx[2])*math.cos(self.ry*math.pi/180))
            
            # Calculation of rotation about z
            Rz = ((Ry[0])*math.cos(self.rz*math.pi/180) + (Ry[1])*math.sin(self.rz*math.pi/180), 
                  (Ry[0])*-math.sin(self.rz*math.pi/180) + (Ry[1])*math.cos(self.rz*math.pi/180), 
                   Ry[2])

            dispX = 300+ Rz[0]
            dispY = 300+ Rz[1]
            
            pygame.draw.circle(screen, self.colour, (dispX, dispY), 2)
            points.append((dispX, dispY))
        
        R = int(127.5 * (1 + math.sin(t + 0)))
        G = int(127.5 * (1 + math.sin(t + 2 * math.pi / 3)))
        B = int(127.5 * (1 + math.sin(t + 4 * math.pi / 3)))
        # Draw edge lines
        for line in self.edges:
            startI = line[0]
            endI = line[1]
            # use indexes to get positions
            startP = points[startI]
            endP = points[endI]

            # draw lines
            pygame.draw.line(screen, (R,G,B), startP, endP, 2)

# Initialise pygame
pygame.init()
screen = pygame.display.set_mode((600, 600), 0, 32)

st, et = 0, 0
t = 0

# Open model from file
with open("Models/Dodecahedron.txt", "r") as objF:
    vertices, edges = json.load(objF)
    obj = Object((0,0,0), [Vertex(vert) for vert in vertices], edges)

# Game loop
while True:
    dt = et - st
    t += dt
    st = time.time()
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # End loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rotate objects
    obj.rx += 100*dt
    #obj.ry += 100*dt
    obj.rz += 100*dt

    # Draw objects
    obj.draw3D(screen)

    pygame.display.update()
    et = time.time()
    