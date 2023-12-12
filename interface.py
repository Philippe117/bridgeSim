from wood import *
from pave import *
from steel import *
from car import *
from mecanical import *


def connexionCheck(me, node):
    for link in node.links:
        if link.node1 == me or link.node1 == me:
            return True
    for link in me.links:
        if link.node1 == node or link.node1 == node:
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

        self.linkType = WoodLink
        self.nodeType = WoodNode

        self.ghostNodePos = pygame.Vector2(0, 0)

        self.offsetPos = None
        self.onsCar = False

        self.linkables = []

    def pressLeft(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            if self.hovered:
                self.selected = self.hovered
                self.offsetPos = mousePos - self.selected.pos
                self.state = "linking"
            else:
                if self.linkables:
                    # Ajoute un node avec les liens
                    node = self.nodeType(mousePos, world)
                    for linkable in self.linkables:
                        self.linkType(node, linkable, world, )
                else:
                    self.nodeType(mousePos, world)

        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseLeft(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            self.state = "idle"
        elif self.state == "linking":
            diff = self.selected.pos - mousePos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
            if self.hovered and self.hovered != self.selected and not connexionCheck(self.selected,
                                                                                     self.hovered) and dist < self.linkType.maxLength:
                # Ajoute un lien
                self.linkType(self.hovered, self.selected, world)
            else:
                # Ajoute un node avec un lien
                node = self.nodeType(self.ghostNodePos, world)
                self.linkType(node, self.selected, world)

            self.selected = None
            self.state = "idle"
        elif self.state == "deleting":
            pass

    def pressRight(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            self.state = "deleting"
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseRight(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            self.state = "idle"

    def pressMiddle(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            if self.hovered:
                self.selected = self.hovered
                self.offsetPos = mousePos - self.selected.pos
                self.state = "dragging"
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseMiddle(self, world):
        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), world.screen)
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            self.state = "idle"
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def update(self, world, screen, running):

        mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom
                world.camera.zoom *= 1 + event.y * 0.1
                world.camera.pos += (mousePos - world.camera.pos) * (event.y * 0.1)

        # Obtention de l'état de la sourie
        left, middle, right = pygame.mouse.get_pressed()

        if left and not self.oldLeft:
            self.pressLeft(world)
        elif not left and self.oldLeft:
            self.releaseLeft(world)

        if right and not self.oldRight:
            self.pressRight(world)
        elif not right and self.oldRight:
            self.releaseRight(world)

        if middle and not self.oldMiddle:
            self.pressMiddle(world)
        elif not middle and self.oldMiddle:
            self.releaseMiddle(world)

        self.oldLeft = left
        self.oldRight = right
        self.oldMiddle = middle

        self.hovered = None
        # Obtien la liste des points à proximité du curseur
        proximities = world.getNodesInRange(mousePos, self.linkType.maxLength)
        self.linkables = []
        if proximities:
            # Détermine quel nodes peuvent être connectés
            for proximity in proximities[:3]:
                self.linkables.append(proximity["node"])

            if proximities[0]["dist"] < proximities[0]["node"].radius:
                self.hovered = proximities[0]["node"]

        if self.state == "idle":
            if self.allowAddNode:
                pass
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                self.linkType = WoodLink
                self.nodeType = WoodNode
            elif keys[pygame.K_2]:
                self.linkType = PaveLink
                self.nodeType = PaveNode
            elif keys[pygame.K_3]:
                self.linkType = CarLink
                self.nodeType = CarNode
            elif keys[pygame.K_4]:
                self.linkType = CarLink
                self.nodeType = TireNode
            elif keys[pygame.K_5]:
                self.linkType = SteelLink
                self.nodeType = SteelNode
            elif keys[pygame.K_6]:
                self.linkType = JackLink
                self.nodeType = JackNode
            elif keys[pygame.K_7]:
                self.linkType = PullerLink
                self.nodeType = JackNode
            elif keys[pygame.K_0] and not self.onsCar:
                pos = pygame.Vector2(-18, -0.7)
                size = pygame.Vector2(3, 1)
                Car(pos, size, world)
            self.onsCar = keys[pygame.K_0]
        # Permet de déplacer un node avec la sourie
        elif self.state == "dragging":
            if self.selected:
                if self.selected.deleteFlag:
                    self.selected = None
                else:
                    # self.selected.force += (mousePos + self.offsetPos - self.selected.pos) * 80000 - self.selected.vel * 1000
                    self.selected.force += (
                                               mousePos - self.offsetPos - self.selected.pos) * 1000 - self.selected.vel * 100

        elif self.state == "linking":

            if self.selected.deleteFlag:
                self.selected = None
            else:
                diff = mousePos - self.selected.pos
                dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
                if dist <= 0:
                    self.ghostNodePos = self.selected.pos
                elif dist > self.linkType.maxLength:
                    self.ghostNodePos = self.selected.pos + diff / dist * self.linkType.maxLength
                elif dist < self.linkType.minLength:
                    self.ghostNodePos = self.selected.pos + diff / dist * self.linkType.minLength
                else:
                    self.ghostNodePos = mousePos


        elif self.state == "deleting":
            # Supprime les nodes
            if self.hovered and not self.hovered.indestructible:
                self.hovered.delete()

        return running

    def draw(self, world):

        # Affiche la selection
        img = self.font.render("hovered: " + str(self.hovered), True, "#000000")
        world.screen.blit(img, pygame.Vector2(10, 10))

        img = self.font.render("selected: " + str(self.selected), True, "#000000")
        world.screen.blit(img, pygame.Vector2(10, 30))

        img = self.font.render("LinkTool: " + str(self.linkType), True, "#000000")
        world.screen.blit(img, pygame.Vector2(10, 50))
        img = self.font.render("NodeTool: " + str(self.nodeType), True, "#000000")
        world.screen.blit(img, pygame.Vector2(10, 70))

        if self.state == "idle":
            if self.allowAddNode:
                # Dessine les liens possibles
                for node in self.linkables:
                    pos = world.camera.posToScreen(node.pos, world.screen)
                    pygame.draw.line(world.screen, "#ff8800", pos, pygame.mouse.get_pos())

        elif self.state == "dragging":
            if self.selected:
                pos = world.camera.posToScreen(self.selected.pos, world.screen)
                pygame.draw.line(world.screen, "#ffffff", pos, pygame.mouse.get_pos())
            else:
                self.state = "idle"

        elif self.state == "linking":
            if self.selected:
                pos = world.camera.posToScreen(self.selected.pos, world.screen)
                ghostPos = world.camera.posToScreen(self.ghostNodePos, world.screen)
                pygame.draw.circle(world.screen, "#ffffff", pos, self.linkType.maxLength * world.camera.zoom, 1)
                pygame.draw.circle(world.screen, "#ffffff", ghostPos, 0.2 * world.camera.zoom, 1)
                pygame.draw.line(world.screen, "#ffffff", pos, pygame.mouse.get_pos())
            else:
                self.state = "idle"

        elif self.state == "deleting":
            pass
