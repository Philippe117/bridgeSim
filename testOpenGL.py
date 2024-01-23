import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi

# Fonction pour convertir une couleur hexadécimale en valeurs décimales
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

# Fonction pour dessiner le périmètre d'un cercle avec une couleur spécifiée


def loadImage(imagePath):
    # Chargement de l'image PNG
    imagePath = "ressources/pickup.png"
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
def drawImage(texture_id, x, y, width, height, angle):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glRotatef(180-angle, 0.0, 0.0, 1.0)  # Appliquer la rotation autour de l'axe Z
    glTranslatef(-x - 0.5*width, -y - 0.5*height, 0.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+width, y)
    glTexCoord2f(1, 1); glVertex2f(x+width, y+height)
    glTexCoord2f(0, 1); glVertex2f(x, y+height)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Initialisation de OpenGL
glOrtho(0, width, height, 0, -1, 1)


texture_id = loadImage("ressources/pickup.png")


# Position initiale et angle de l'image
#image_x, image_y = 200, 200
#image_width, image_height = image_surface.get_width(), image_surface.get_height()
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
    drawImage(texture_id, 100, 0, 100, 50, image_angle)
    image_angle += 2
    pygame.display.flip()
    pygame.time.wait(10)  # Pause pour contrôler la vitesse de rafraîchissement

# N'oubliez pas de quitter Pygame à la fin
pygame.quit()
