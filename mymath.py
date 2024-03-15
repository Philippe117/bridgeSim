import pygame


def getDiffLengthUnitNorm(pos1, pos2):
    diff = pos2 - pos1
    length = (diff.x ** 2 + diff.y ** 2) ** 0.5

    if length > 0:
        unit = diff /length
    else:
        unit = pygame.Vector2(1, 0)

    norm = pygame.Vector2(unit.y, -unit.x)
    return diff, length, unit, norm
    #raise ValueError('Impossible de updateValues'+str(pos1)+" : "+str(pos2))


def newGroups(nb):
    list = []
    for i in range(nb):
        list.append([])
    return list
