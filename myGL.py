
from OpenGL.GL import (glColor3f, glLineWidth, glBegin,glVertex2f, glEnd, GL_LINES,
                       GL_QUADS, GL_TRIANGLE_FAN, GL_LINE_LOOP)
from math import sin, cos
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi


# Fonction pour convertir une couleur hexadécimale en valeurs décimales
def setColorHex(color):
    color = hexToColor(color)
    glColor3f(color[0], color[1], color[2])

def hexToColor(color):
    hex_color = color.lstrip("#")
    color = tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return color

# Fonction pour dessiner une ligne
def drawLine(pos1, pos2, width=-1):
    if width > 0:
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex2f(pos1.x, pos1.y)
        glVertex2f(pos2.x, pos2.y)
        glEnd()

# Fonction pour dessiner un carré
def drawSquare(pos, size):
    glBegin(GL_QUADS)
    glVertex2f(pos.x, pos.y)
    glVertex2f(pos.x + size, pos.y)
    glVertex2f(pos.x + size, pos.y + size)
    glVertex2f(pos.x, pos.y + size)
    glEnd()

# Fonction pour dessiner un cercle
def drawDisk(pos, radius, num_segments=100):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(pos.x, pos.y)
    for i in range(num_segments + 1):
        theta = i * (2.0 * 3.1415926 / num_segments)
        dx = radius * cos(theta)
        dy = radius * sin(theta)
        glVertex2f(pos.x + dx, pos.y + dy)
    glEnd()

    # Fonction pour dessiner un cercle
def drawCircle(pos, radius, num_segments=100, width=-1):
    if width > 0:
        glLineWidth(width)
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments):
            theta = i * (2.0 * 3.1415926 / num_segments)
            dx = radius * cos(theta)
            dy = radius * sin(theta)
            glVertex2f(pos.x + dx, pos.y + dy)
        glEnd()


def loadImage(imagePath):
    # Chargement de l'image PNG
    imageSurface = pygame.image.load(imagePath)
    imageData = pygame.image.tostring(imageSurface, "RGBA", 1)

    # Création d'une texture OpenGL
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imageSurface.get_width(), imageSurface.get_height(), 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, imageData)
    return texture_id

# Fonction pour dessiner une image en rotation autour de son centre
def drawImage(image, pos, size, angle=0):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, image)

    glPushMatrix()
    glTranslatef(pos.x, pos.y, 0.0)
    glRotatef(angle*180/3.14159, 0.0, 0.0, 1.0)  # Appliquer la rotation autour de l'axe Z
    glTranslatef(- 0.5 * size.x, - 0.5 * size.y, 0.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(0, 0)
    glTexCoord2f(1, 1); glVertex2f(size.x, 0)
    glTexCoord2f(1, 0); glVertex2f(size.x, size.y)
    glTexCoord2f(0, 0); glVertex2f(0, size.y)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

# Example:
# def draw(self, camera):
#     # Position initiale du carré
#     glColor3f(1, 0, 0)
#     drawSquare(camera.posToScreen(pygame.Vector2(0, 0)), 1*camera.zoom)
#     glColor3f(1, 1, 0)
#     drawCircle(camera.posToScreen(pygame.Vector2(2, 0)), 1*camera.zoom, num_segments=6)
#     image = loadImage("ressources/pickup.png")
#     glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
#     drawImage(image, 100, 100, 100, 50, 0)

if __name__ == "__main__":
    # Initialisation de Pygame
    pygame.init()

    # Définition de la taille de la fenêtre
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    # Initialisation de OpenGL
    glOrtho(0, width, height, 0, -1, 1)


    texture_id = loadImage("ressources/pickup.png")

    image_angle = 0.0  # Angle en degrés

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT)

        # Dessiner l'image en rotation autour de son centre
        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(texture_id, pygame.Vector2(100, 100), pygame.Vector2(100, 100), image_angle)
        image_angle += 2
        pygame.display.flip()
        pygame.time.wait(10)  # Pause pour contrôler la vitesse de rafraîchissement

    # N'oubliez pas de quitter Pygame à la fin
    pygame.quit()

