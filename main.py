import sys
import math
import time
import pygame

class Vertex():
    def __init__(self, posX, posY, posZ):
        # Store position of one Vertex
        self.x = posX
        self.y = posY
        self.z = posZ

class Object():
    # 3D Object with a pivot, verticies and edges
    def __init__(self, cntre, verts, edgs, col=(255,255,255)):
        self.x = cntre[0]
        self.y = cntre[1]
        self.z = cntre[2]

        self.verticies = verts  # Store positions of vertexes in a list
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
        for vert in self.verticies:
            # Matrix approach
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

            dispX = 400+ Rz[0]
            dispY = 300+ Rz[1]
            
            pygame.draw.circle(screen, self.colour, (dispX, dispY), 2)
            points.append((dispX, dispY))
        
        # Draw edge lines
        for line in self.edges:
            startI = line[0]
            endI = line[1]
            # use indexes to get positions
            startP = points[startI]
            endP = points[endI]

            # draw lines
            pygame.draw.line(screen, self.colour, startP, endP, 2)

# Initialisations
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

st, et = 0, 0

# Cube Object
centre = (0,0,0)
vertices =[Vertex(50, 50, 50),  Vertex(-50, 50, 50),
            Vertex(50,-50, 50),  Vertex(-50,-50, 50),
            Vertex(50, 50,-50),  Vertex(-50, 50,-50),
            Vertex(50,-50,-50),  Vertex(-50,-50,-50)]
edges = ([0,1], [0,2], [0,4],
         [3,1], [3,2], [3,7],
         [5,4], [5,7], [5,1],
         [6,7], [6,4], [6,2])
Cube = Object(centre, vertices, edges)

# Triangle object
centre = (0,0,0)
vertices =[Vertex(50, -50, 50),  Vertex(-50, -50, 50),
            Vertex(50,-50, -50),  Vertex(-50,-50, -50),
            Vertex(0, 50,0)]
edges = ([0,1], [0,2],
         [3,1], [3,2],
         [0,4], [1,4],
         [2,4], [3,4])

Pyramid = Object(centre, vertices, edges)

# Prism object
centre = (0,0,0)
vertices =[Vertex(100, -50, 50),  Vertex(-50, -50, 50),
            Vertex(100,-50, -50),  Vertex(-50,-50, -50),
            Vertex(100, 50,0), Vertex(-50, 50,0)]
edges = ([0,1], [0,2],
         [3,1], [3,2],
         [0,4], [1,5],
         [2,4], [3,5],
         [4,5])

Prism = Object(centre, vertices, edges)

# Game loop
while True:
    dt = et - st
    st = time.time()
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # End loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    Cube.rx += 100* dt
    Cube.ry += 100* dt
    Cube.rz += 100* dt

    Pyramid.rx += 100* dt
    Pyramid.ry += 100* dt
    Pyramid.rz += 100* dt

    Prism.rx += 100* dt
    Prism.ry += 100* dt
    Prism.rz += 100* dt

    #Cube.draw3D(screen)
    #Pyramid.draw3D(screen)
    Prism.draw3D(screen)

    pygame.display.update()
    et = time.time()
    