import sys
import math
import time
import pygame
import json
import os

class Vertex():
    def __init__(self, pos):
        # Store position of one Vertex
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

class Object():
    # 3D Object with a pivot, vertices and edges
    def __init__(self, cntr, verts, faces):
        self.x = cntr[0]
        self.y = cntr[1]
        self.z = cntr[2]

        self.vertices = verts  # Store positions of vertexes in a list
        self.faces = faces # Faces with 3 vertices with a colour in hex

        # rotation of object by all 3 axis
        # in degrees
        self.rx = 0
        self.ry = 0
        self.rz = 0
    
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
            dispZ = Rz[2]
            
            #pygame.draw.circle(screen, (255,255,255), (dispX, dispY), 2)
            points.append((dispX, dispY, dispZ))
        
        R = int(127.5 * (1 + math.sin(t + 0)))
        G = int(127.5 * (1 + math.sin(t + 2 * math.pi / 3)))
        B = int(127.5 * (1 + math.sin(t + 4 * math.pi / 3)))

        for face in self.faces:
            self.DrawFace(screen, face, points)
        

    def DrawFace(self, screen, face, points):
        hex = face[0]
        C1 = points[face[1]]
        C2 = points[face[2]]
        C3 = points[face[3]]

        N = CalculateSurfaceNormal(C1,C2,C3)

        if N[2] < 0:
            return
        
        shade = min(math.sqrt(N[2])/100,1)
        col = (int(hex[0:2], 16)*shade, int(hex[2:4], 16)*shade, int(hex[4:], 16)*shade)

        #pygame.draw.line(screen, (255,255,255), C1[:2], C2[:2], 2)
        #pygame.draw.line(screen, (255,255,255), C2[:2], C3[:2], 2)
        #pygame.draw.line(screen, (255,255,255), C1[:2], C3[:2], 2)
        pygame.draw.polygon(screen, col, (C1[:2], C2[:2], C3[:2]))
        
        
def CalculateSurfaceNormal(C1,C2,C3):
    # Calculate Surface normals
    A = [
        C2[0] - C1[0],
        C2[1] - C1[1],
        C2[2] - C1[2]
        ]
    B = [
        C3[0] - C1[0],
        C3[1] - C1[1],
        C3[2] - C1[2]
    ]
    N = [
        A[1]*B[2] - A[2]*B[1],
        A[2]*B[0] - A[0]*B[2],
        A[0]*B[1] - A[1]*B[0]
    ]
    return N


def Update(dt, k):
    global curr, obj
    if k == None:
        return
        
    # Rotate objects
    obj.rx += 100*dt if k[pygame.K_k] else 0
    obj.rx -= 100*dt if k[pygame.K_i] else 0
    obj.ry += 100*dt if k[pygame.K_l] else 0
    obj.ry -= 100*dt if k[pygame.K_j] else 0
    obj.rz += 100*dt if k[pygame.K_u] else 0
    obj.rz -= 100*dt if k[pygame.K_o] else 0

    # Change Object pointer
    curr += 10*dt if k[pygame.K_RIGHT] else 0
    curr -= 10*dt if k[pygame.K_LEFT] else 0

    # Get the Object properties and swap it out
    vertices, faces = GetObject(curr)
    obj.vertices = vertices
    obj.faces = faces

def GetObject(curr):
    allObj= [file for file in os.listdir("Models/") if os.path.isfile(os.path.join("Models/", file))]
    n = int(curr%len(allObj))

    # Open model from file
    with open(f"Models/{allObj[n]}", "r") as objF:
        vertices, faces = json.load(objF)
    return [Vertex(vert) for vert in vertices], faces

def displayText(screen, text, pos=(50,50), font=None, color=(255, 255, 255)):
    font = pygame.font.SysFont('None', 32) if font == None else font
    info_surface = font.render(text, False, color)
    screen.blit(info_surface, pos)

# Initialise pygame
pygame.init()
screen = pygame.display.set_mode((600, 600), 0, 32)
pygame.font.init()

st, et = 0, 0
t = 0
n = 0
fps = 0
k = None

# Initialise the Object
curr = 0
vertices, edges = GetObject(curr)
obj = Object((0,0,0), vertices, edges)

# Game loop
while True:
    dt = et - st
    t += dt
    n += 1
    st = time.time()
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # End loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Store inputs in the list k
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            k = pygame.key.get_pressed()
        if event.type == pygame.KEYUP:
            k = pygame.key.get_pressed()

    # Handle user input
    Update(dt,k)

    # Draw objects
    obj.draw3D(screen)

    # Debug info
    if n % 1000 == 0:
        fps = round(n/t)
    displayText(screen, f"fps: {fps}, rx: {round(obj.rx,1)}, ry: {round(obj.ry,1)}, rz: {round(obj.rz,1)}")

    pygame.display.update()
    et = time.time()
    