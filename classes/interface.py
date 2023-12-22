from classes.wood import *
from classes.pave import *
from classes.steel import *
from classes.car import *
from classes.mecanical import *
from copy import copy


def connexionCheck(me, node):
    for link in node.links:
        if link.node1 == me or link.node2 == me:
            return link
    for link in me.links:
        if link.node1 == node or link.node2 == node:
            return link
    return None


class Interface:

    def __init__(self, camera):

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
        self.camera = camera

        self.linkType = WoodLink
        self.nodeType = WoodNode

        self.ghostNodePos = pygame.Vector2(0, 0)

        self.offsetPos = None
        self.onsCar = False

        self.gridResolution = 100

        self.linkables = []

    def pressLeft(self, world, mousePos):
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
                        self.linkType(node1=node, node2=linkable, world=world )
                else:
                    self.nodeType(mousePos, world)

        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseLeft(self, world, mousePos):
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            self.state = "idle"
        elif self.state == "linking":
            diff = self.selected.pos - mousePos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5


            if self.hovered and self.hovered != self.selected and dist < self.linkType.maxLength:
                link = connexionCheck(self.selected, self.hovered)
                print()
                if link and Destructible in type(link).__bases__:
                    link.delete()
                    self.linkType(node1=self.hovered, node2=self.selected, world=world)
                    if Destructible in type(self.hovered).__bases__:
                        links = copy(self.hovered.links)
                        self.hovered.links = []
                        newNode = self.nodeType(self.hovered.pos, self.hovered.world)
                        newNode.age = self.hovered.age
                        for link in links:
                            if link.node1 == self.hovered:
                                link.connectNode1(newNode)
                            if link.node2 == self.hovered:
                                link.connectNode2(newNode)
                        self.hovered.delete()
                        self.hovered = newNode
                else:
                    self.linkType(node1=self.hovered, node2=self.selected, world=world)


            else:
                # Ajoute un node avec un lien
                node = self.nodeType(self.ghostNodePos, world)
                self.linkType(node1=node, node2=self.selected, world=world)

            self.selected = None
            self.state = "idle"
        elif self.state == "deleting":
            pass

    def pressRight(self, world, mousePos):
        if self.state == "idle":
            self.state = "deleting"
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def releaseRight(self, world, mousePos):
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            pass
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            self.state = "idle"

    def pressMiddle(self, world, mousePos):
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

    def releaseMiddle(self, world, mousePos):
        if self.state == "idle":
            pass
        elif self.state == "dragging":
            self.state = "idle"
        elif self.state == "linking":
            pass
        elif self.state == "deleting":
            pass

    def update(self, world, camera, running):
        mousePos = self.camera.screenToPos(pygame.mouse.get_pos())
        mousePos.x = round(mousePos.x*self.gridResolution, 0)/self.gridResolution
        mousePos.y = round(mousePos.y*self.gridResolution, 0)/self.gridResolution

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.linkType = WoodLink
            self.nodeType = WoodNode
        elif keys[pygame.K_2]:
            self.linkType = PaveLink
            self.nodeType = PaveNode
        elif keys[pygame.K_3]:
            self.linkType = SteelLink
            self.nodeType = SteelNode
        elif keys[pygame.K_4]:
            self.linkType = JackLink
            self.nodeType = JackNode
        elif keys[pygame.K_5]:
            self.linkType = PullerLink
            self.nodeType = JackNode
        elif keys[pygame.K_6]:
            self.linkType = SpringLink
            self.nodeType = JackNode
        elif keys[pygame.K_7]:
            pass
        elif keys[pygame.K_8]:
            pass
        elif keys[pygame.K_9]:
            pass
        elif keys[pygame.K_0] and not self.onsCar:
            pos = pygame.Vector2(-18, -0.7)
            size = pygame.Vector2(3, 1)
            Car(pos, size, world)
        self.onsCar = keys[pygame.K_0]



        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:

                toInteract = world.getInteractibles(mousePos)
                if toInteract and len(toInteract) > 0:
                    for interactible in toInteract:
                        interactible.sclollAction(event.y)
                else:

                    # Zoom
                    camera.zoom *= 1 + event.y * 0.1
                    camera.pos += (mousePos - camera.pos) * (event.y * 0.1)

        # Obtention de l'état de la sourie
        left, middle, right = pygame.mouse.get_pressed()

        if left and not self.oldLeft:
            self.pressLeft(world, mousePos)
        elif not left and self.oldLeft:
            self.releaseLeft(world, mousePos)

        if right and not self.oldRight:
            self.pressRight(world, mousePos)
        elif not right and self.oldRight:
            self.releaseRight(world, mousePos)

        if middle and not self.oldMiddle:
            self.pressMiddle(world, mousePos)
        elif not middle and self.oldMiddle:
            self.releaseMiddle(world, mousePos)

        self.oldLeft = left
        self.oldRight = right
        self.oldMiddle = middle

        self.hovered = None
        # Obtien la liste des points à proximité du curseur
        proximities = world.getLinkables(mousePos, self.linkType.maxLength)
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

            for destructible in world.destructibles:
                pos, force = destructible.getContactPos(mousePos, 0.01)
                if pos:
                    destructible.delete()

        return running

    def draw(self, camera):

        mousePos = camera.screenToPos(pygame.mouse.get_pos())
        mousePos.x = round(mousePos.x*self.gridResolution, 0)/self.gridResolution
        mousePos.y = round(mousePos.y*self.gridResolution, 0)/self.gridResolution
        mousePos = camera.posToScreen(mousePos)


        # Affiche la selection
        img = self.font.render("hovered: " + str(self.hovered), True, "#000000")
        camera.screen.blit(img, pygame.Vector2(10, 10))

        img = self.font.render("selected: " + str(self.selected), True, "#000000")
        camera.screen.blit(img, pygame.Vector2(10, 30))

        img = self.font.render("LinkTool: " + str(self.linkType), True, "#000000")
        camera.screen.blit(img, pygame.Vector2(10, 50))
        img = self.font.render("NodeTool: " + str(self.nodeType), True, "#000000")
        camera.screen.blit(img, pygame.Vector2(10, 70))

        if self.state == "idle":
            if self.allowAddNode:
                # Dessine les liens possibles
                for node in self.linkables:
                    pos = camera.posToScreen(node.pos)
                    pygame.draw.line(camera.screen, "#ff8800", pos, mousePos)

        elif self.state == "dragging":
            if self.selected:
                pos = camera.posToScreen(self.selected.pos)
                pygame.draw.line(camera.screen, "#ffffff", pos, mousePos)
            else:
                self.state = "idle"

        elif self.state == "linking":
            if self.selected:
                pos = camera.posToScreen(self.selected.pos)
                ghostPos = camera.posToScreen(self.ghostNodePos)
                pygame.draw.circle(camera.screen, "#ffffff", pos, self.linkType.maxLength * camera.zoom, 1)
                pygame.draw.circle(camera.screen, "#ffffff", ghostPos, 0.2 * camera.zoom, 1)
                pygame.draw.line(camera.screen, "#ffffff", pos, mousePos)
            else:
                self.state = "idle"

        elif self.state == "deleting":
            pass

        # max = 20
        # for x in range(-max, max):
        #     pos1 = camera.posToScreen(pygame.Vector2(x, -max))
        #     pos2 = camera.posToScreen(pygame.Vector2(x, max))
        #     pygame.draw.line(camera.screen, "#ffffff", pos1, pos2)
        # for y in range(-max, max):
        #     pos1 = camera.posToScreen(pygame.Vector2(-max, y))
        #     pos2 = camera.posToScreen(pygame.Vector2(max, y))
        #     pygame.draw.line(camera.screen, "#ffffff", pos1, pos2)