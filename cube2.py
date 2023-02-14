import pygame
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

global level
level = 0

drawedges=False
drawsurfaces=True

vertices = [
    (1.0, -1.0, -1.0),
    (1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (1.0, -1.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 1.0, 1.0),
    (-1.0, -1.0, 1.0)

]


colors = []

surfaces = [
    (0, 1, 2),
    (0, 2, 3),
    (3, 2, 6),
    (3, 6, 7),
    (7, 6, 5),
    (7, 5, 4),
    (4, 5, 1),
    (4, 1, 0),
    (1, 5, 6),
    (1, 6, 2),
    (4, 0, 3),
    (4, 3, 7),

]
real_surfaces = [(0, len(surfaces))]

edges = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 4),
    (1, 5),
    (2, 1),
    (2, 3),
    (2, 6),
    (3, 4),
    (3, 6),
    (7, 3),
    (7, 4),
    (7, 6),
    (5, 1),
    (5, 4),
    (5, 6),
    (5, 7),
]


def cube():
    if drawsurfaces ==True:
        glBegin(GL_TRIANGLES)
        x = 0
        # Find the first Index of surfaces actually still existing, since there are older ones
        y = real_surfaces[len(real_surfaces) - 1][0]

        for surface in surfaces[y:]:
            for vertex in surface:
                x += 1
                if x == len(colors)-1:
                    x = 0
                glColor3fv(colors[x])
                glVertex3fv(vertices[vertex])
        glEnd()
    
    if drawedges == True:
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor3fv(colors[-1:])
                glVertex3fv(vertices[vertex])
        glEnd()

    


def calc_dist(x, y):
    a = vertices[x]
    b = vertices[y]

    dist = math.sqrt(pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2) + pow((a[2] - b[2]), 2))
    return dist

def generate_colors(n):
    global colors
    colorlist = np.random.uniform(low=0.0, high=1.0, size=(n,3))
    colors = colorlist.tolist()

def subdivide():
    global surfaces
    print("Edges davor: ", len(edges), ", Vertices davor: ", len(vertices), ", Surfaces davor: ", len(surfaces))

    new_surfaces = surfaces.copy()
    for surface in surfaces:
        a = surface[0]
        b = surface[1]
        c = surface[2]

        d = len(vertices)

        # Calculate the longest edge and calculate midpoint of it
        dist1 = calc_dist(a, b)
        dist2 = calc_dist(a, c)
        dist3 = calc_dist(b, c)
        if dist1 == dist2:

            vertices.append(((vertices[c][0] + vertices[b][0]) / 2, (vertices[c][1] + vertices[b][1]) / 2,
                             (vertices[c][2] + vertices[b][2]) / 2))
            # Create new surfaces
            new_surfaces.append((a, d, c))
            new_surfaces.append((a, b, d))
            edges.append((a, d))

        elif dist2 == dist3:
            vertices.append(((vertices[a][0] + vertices[b][0]) / 2, (vertices[a][1] + vertices[b][1]) / 2,
                             (vertices[a][2] + vertices[b][2]) / 2))
            # Create new surfaces
            new_surfaces.append((a, d, c))
            new_surfaces.append((b, c, d))
            # Create new edges
            edges.append((c, d))
        else:
            vertices.append(((vertices[a][0] + vertices[c][0]) / 2, (vertices[a][1] + vertices[c][1]) / 2,
                             (vertices[a][2] + vertices[c][2]) / 2))
            # Create new surfaces
            new_surfaces.append((a, b, d))
            new_surfaces.append((b, c, d))
            # Create new edges
            edges.append((b, d))

    # Update the global surfaces list
    surfaces = new_surfaces

    # Update the global realsurfaces list
    y = real_surfaces[-1][1]
    z = len(surfaces)
    real_surfaces.append((y, z))

    print("Edges nach divide: ", len(edges), ", Vertices nach divide: ", len(vertices), ", Surfaces nach divide: ", len(surfaces))
    print(real_surfaces)

def subdivide_back():
    global level

    if level > 0:
        global surfaces
        global vertices
        global real_surfaces
        global edges

        # Update real_surfaces list
        real_surfaces = real_surfaces[:-1]

        # Update surfaces list with real_surfaces help
        y = real_surfaces[-1][1]
        surfaces = surfaces[:y]

        # Update edges and vertices list
        edges = edges[:len(edges)-y]
        vertices = vertices[:len(vertices)-y]

        print("Edges nach back_divide: ", len(edges), ", Vertices nach back_divide: ", len(vertices), ", Surfaces nach back_divide: ", len(surfaces))


def main():
    global level
    global drawsurfaces
    global drawedges
    global colors
    width=800
    height=600

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    glRotatef(25, 2, 1, 0)

    x_angle = 0
    y_angle = 0
    z_angle = 0

    generate_colors(len(vertices))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                #Centers mouseposition
                if event.button == 3:
                    pygame.mouse.set_pos((width/2, height/2))

            if pygame.mouse.get_pressed()[2] == 1: 
                #Spin the cube with mouse movement
                x, y = pygame.mouse.get_rel()
                if pygame.mouse.get_pressed()[2] == 1:
                    glRotatef(x, 0, 1, 0)
                    glRotatef(y, 1, 0, 0)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)

                if event.key == pygame.K_UP:
                    glTranslatef(0, 1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_1:
                    drawedges = not drawedges
                if event.key == pygame.K_2:
                    drawsurfaces = not drawsurfaces
                if event.key == pygame.K_0:
                    glLoadIdentity()
                    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
                    glTranslatef(0.0,0.0, -5)
                    x_angle = 0
                    y_angle = 0
                    z_angle = 0
                if event.key == pygame.K_q:
                    level += 1
                    # print("vertices vor subdivide")
                    # print(len(vertices))
                    subdivide()
                    # print("vertices nach subdivide")
                    # print(len(vertices))
                if event.key == pygame.K_r:
                    subdivide_back()
                    level -= 1
                    if level <= 0:
                        level = 0
                if event.key == pygame.K_c:
                    generate_colors(100)
               

        glEnable(GL_CULL_FACE)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(x_angle, 1, 0, 0)
        glRotatef(y_angle, 0, 1, 0)
        glRotatef(z_angle, 0, 0, 1)
        cube()
        glCullFace(GL_FRONT)
        pygame.display.flip()
        pygame.time.wait(10)
        glDisable(GL_CULL_FACE)
        

main()