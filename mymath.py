import pygame


def getDiffLengthUnitNorm(pos1, pos2):
    if pos1 != pos2:
        diff = pos2 - pos1
        length = (diff.x ** 2 + diff.y ** 2) ** 0.5
        unit = diff /length
        norm = pygame.Vector2(unit.y, -unit.x)
        return diff, length, unit, norm
    else:
        raise ValueError('Impossible de updateValues'+str(pos1)+" : "+str(pos2))


def newGroups(nb):
    list = []
    for i in range(nb):
        list.append([])
    return list
