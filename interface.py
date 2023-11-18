import pygame
from node import Node
from link import Link

def connexionCheck(me, node):
    for link in node.links:
        if link.node1 == me or link.node1 == me:
            return True
    return False

class Interface:


    def __init__(self):

        self.allowZoom = True
        self.allowPan = True
        self.allowAddNode = True
        self.allowAddLink = True
        self.allowAddLink = True
        self.allowMoveNode = False

        self.enabled = True
        self.state = "idle"  # idle, dragging, deleting, linking,

        self.font = pygame.font.SysFont("silomttf", 20)

        self.selected = None
        self.hovered = None
        self.oldLeft = False
        self.oldRight = False
        self.oldMiddle = False

        self.offsetPos = None

        self.linkables = []

    def pressLeft(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            if self.hovered:
                self.selected = self.hovered
                self.offsetPos = mousePos - self.selected.pos
                self.state = "linking"
            else:
                if self.linkables:
                    # Ajoute un node avec les liens
                    node = Node(mousePos)
                    world.nodes.append(node)
                    for linkable in self.linkables:
                        world.links.append(Link(node, linkable))

        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseLeft(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            self.state = "idle"
        elif self.state == "linking":
            if self.hovered and self.hovered != self.selected and not connexionCheck(self.selected, self.hovered):
                # Ajoute un lien
                world.links.append(Link(self.hovered, self.selected))
            elif not self.hovered:
                # Ajoute un node avec un lien
                node = Node(mousePos)
                world.nodes.append(node)
                world.links.append(Link(node, self.selected))

            self.selected = None
            self.state = "idle"
        elif self.state == "deleting":
            pass

    def pressRight(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            self.state = "deleting"
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseRight(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            self.state = "idle"

    def pressMiddle(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseMiddle(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def update(self, world, screen):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)


        # Obtention de l'état de la sourie
        left, middle, right = pygame.mouse.get_pressed()

        if left and not self.oldLeft:
            self.pressLeft(world, screen)
        elif not left and self.oldLeft:
            self.releaseLeft(world, screen)

        if right and not self.oldRight:
            self.pressRight(world, screen)
        elif not right and self.oldRight:
            self.releaseRight(world, screen)

        if middle and not self.oldMiddle:
            self.pressMiddle(world, screen)
        elif not middle and self.oldMiddle:
            self.releaseMiddle(world, screen)

        self.oldLeft = left
        self.oldRight = right
        self.oldMiddle = middle


        self.hovered = None
        # Obtien la liste des points à proximité du curseur
        proximities = world.getNodesInRange(mousePos, 2)
        self.linkables = []
        if proximities:
            # Détermine quel nodes peuvent être connectés
            for proximity in proximities[:3]:
                self.linkables.append(proximity["node"])

            if proximities[0]["dist"] < proximities[0]["node"].size:
                self.hovered = proximities[0]["node"]



        if self.state == "idle":
            if self.allowAddNode:
                pass

        # Permet de déplacer un node avec la sourie
        elif self.state == "dragging":
            if self.selected:
                if self.selected.deleteFlag:
                    self.selected = None
                else:
                    self.selected.force += (mousePos+self.offsetPos-self.selected.pos)*10000-self.selected.vel*1000

        elif self.state == "linking":
            if self.selected.deleteFlag:
                self.selected = None

        elif self.state == "deleting":
            # Supprime les nodes
            if self.hovered:
                self.hovered.delete()





    def draw(self, world, screen):


        # Affiche la selection
        img = self.font.render("hovered: " + str(self.hovered), True, "#000000")
        screen.blit(img, pygame.Vector2(10, 10))

        img = self.font.render("selected: " + str(self.selected), True, "#000000")
        screen.blit(img, pygame.Vector2(10, 30))


        if self.state == "idle":
            if self.allowAddNode:
                # Dessine les liens possibles
                for node in self.linkables:
                    pos = world.camera.posToScreen(node.pos, screen)
                    pygame.draw.line(screen, "#ff8800", pos, pygame.mouse.get_pos())

        elif self.state == "dragging":
            pos = world.camera.posToScreen(self.selected.pos, screen)
            pygame.draw.line(screen, "#ffffff", pos, pygame.mouse.get_pos())

        elif self.state == "linking":
            pos = world.camera.posToScreen(self.selected.pos, screen)
            pygame.draw.line(screen, "#ffffff", pos, pygame.mouse.get_pos())

        elif self.state == "deleting":
            pass

