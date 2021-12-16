# !/usr/bin/env python3.9

"""
small game for physics project
"""


__author__ = "James Packham"

import random
import sys
from math import atan2, cos, sin, tau
from fractions import Fraction as fr

import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()


class TextBox:
    def __init__(self, coords, text, text_size, font='arial'):
        self.text = text.split('\n')
        self.text_size = text_size
        self.font = pygame.font.SysFont(font, text_size)
        self.coords = coords
        self.size = text_size

    def draw(self, surface):
        for i, line in enumerate(self.text):
            # pygame.draw.rect(surface, 'grey', self.coords)
            rend = self.font.render(line, True, (0, 0, 0))
            surface.blit(rend, (self.coords[0], self.coords[1]+i*self.size))


class Quark:
    def __init__(self, name, symbol, charge, colour, pos, is_anti=False):
        self.name = name
        self.symbol = symbol
        self.charge = charge
        self.colour = colour
        self.anti = is_anti
        self.pos = list(pos)
        self.picked_up = False
        self.box_pos = None
        self.font = pygame.font.SysFont('arial', 20)
        self.rend = self.font.render(self.symbol, True, (0, 0, 0))
        self.linked_customer = None
        self.maker_index = None
        self.am = None
        self.to_remove = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos, 30)

    def put_down(self, pos):
        if pygame.Rect(30, 560, 1220, 110).collidepoint(*self.pos):
            self.pos = list(pos)
            self.picked_up = False
            return True
        if pygame.Rect(30, 360, 210, 140).collidepoint(*self.pos):
            smallest = ((0, 0), POINTS[0][0], distance(self.pos, POINTS[0][0]))
            for a, columns in enumerate(POINTS):
                for b, point in enumerate(columns):
                    if distance(point, self.pos) < smallest[2]:
                        smallest = ((a, b), point, distance(point, self.pos))
            if BOX[smallest[0][0]][smallest[0][1]] is None:
                self.pos = smallest[1]
                self.picked_up = False
                BOX[smallest[0][0]][smallest[0][1]] = self
                self.box_pos = (smallest[0][0], smallest[0][1])
                return True
        for entity in CUSTOMERS:
            if distance(self.pos, entity.pos) < 50:
                self.linked_customer = entity
                self.picked_up = False
                entity.holding = self
                return True
        for i, point in enumerate(hm.points):
            if distance(self.pos, point) < 30:
                if hm.slots[i] is None:
                    self.maker_index = i
                    hm.slots[i] = self
                    self.picked_up = False
                    return True
        if distance(self.pos, am.points) < 50:
            am.slot = self
            self.picked_up = False
            self.am = pos

        return False

    def update(self):
        if self.picked_up:
            self.pos = list(pygame.mouse.get_pos())
        if self.linked_customer is not None:
            self.pos = list(self.linked_customer.pos)
        if self.maker_index is not None:
            self.pos = list(hm.points[self.maker_index])
        if self.am is not None:
            self.pos = list(am.points)
        elif pygame.Rect(30, 560, 1220, 110).collidepoint(*self.pos):
            self.pos[0] += 4


class Up(Quark):
    def __init__(self, pos):
        pos = pos[0], pos[1] + 10
        super(Up, self).__init__('up', 'u', fr(2, 3), 'red', pos)

    def draw(self, surface):
        size = 60
        A = (self.pos[0], self.pos[1] - size * pow(3, 0.5)/3)
        B = (self.pos[0] - size/2, self.pos[1] + size * pow(3, 0.5)/6)
        C = (self.pos[0] + size/2, self.pos[1] + size * pow(3, 0.5)/6)
        pygame.draw.polygon(surface, self.colour, (A, B, C))

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Down(Quark):
    def __init__(self, pos):
        pos = pos[0], pos[1] - 10
        super(Down, self).__init__('down', 'd', fr(-1, 3), 'light blue', pos)

    def draw(self, surface):
        size = 60
        A = (self.pos[0], self.pos[1] + size * pow(3, 0.5)/3)
        B = (self.pos[0] - size/2, self.pos[1] - size * pow(3, 0.5)/6)
        C = (self.pos[0] + size/2, self.pos[1] - size * pow(3, 0.5)/6)
        pygame.draw.polygon(surface, self.colour, (A, B, C))

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))
    

class Top(Quark):
    def __init__(self, pos):
        super(Top, self).__init__('top', 't', fr(2, 3), 'green', pos)

    def draw(self, surface):
        x, y = self.pos
        size = 30
        ang = tau/6
        points = [(x + size * sin(ang * i), y + size * cos(ang * i)) for i in range(6)]

        pygame.draw.polygon(surface, self.colour, points)

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))
        

class Bottom(Quark):
    def __init__(self, pos):
        super(Bottom, self).__init__('bottom', 'b', fr(-1, 3), 'yellow', pos)

    def draw(self, surface):
        x, y = self.pos
        size = 30
        ang = tau/6
        points = [(x + size * sin(ang * i), y + size * cos(ang * i)) for i in range(6)]

        pygame.draw.polygon(surface, self.colour, points)

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Strange(Quark):
    def __init__(self, pos):
        super(Strange, self).__init__('strange', 's', fr(-1, 3), 'pink', pos)

    def draw(self, surface):
        x, y = self.pos
        size = 30
        ang = tau/5
        points = [(x + size * sin(ang * i), y - size * cos(ang * i)) for i in range(5)]

        pygame.draw.polygon(surface, self.colour, points)

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Charm(Quark):
    def __init__(self, pos):
        super(Charm, self).__init__('charm', 'c', fr(2, 3), 'purple', pos)

    def draw(self, surface):
        x, y = self.pos
        size = 30
        ang = tau/5
        points = [(x + size * sin(ang * i), y + size * cos(ang * i)) for i in range(5)]

        pygame.draw.polygon(surface, self.colour, points)

        surface.blit(self.rend, self.rend.get_rect(center=self.pos))
        
        
class Neutron(Quark):
    """not a quark but don't worry about it"""
    def __init__(self, pos):
        super(Neutron, self).__init__('neutron', 'n', fr(0, 1), 'gray64', pos)

    def draw(self, surface):
        super(Neutron, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Proton(Quark):
    """not a quark but don't worry about it"""
    def __init__(self, pos):
        super(Proton, self).__init__('proton', 'p+', fr(1, 1), 'gray64', pos)

    def draw(self, surface):
        super(Proton, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Lambda(Quark):
    def __init__(self, pos):
        super(Lambda, self).__init__('lambda', 'Λ', fr(1, 1), 'gray64', pos)

    def draw(self, surface):
        super(Lambda, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))
        

class Sigma(Quark):
    def __init__(self, pos):
        super(Sigma, self).__init__('sigma', 'Σ', fr(1, 1), 'gray64', pos)

    def draw(self, surface):
        super(Sigma, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Xi(Quark):
    def __init__(self, pos):
        super(Xi, self).__init__('xi', 'Ξ', fr(1, 1), 'gray64', pos)

    def draw(self, surface):
        super(Xi, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class Delta(Quark):
    def __init__(self, pos):
        super(Delta, self).__init__('delta', 'Δ', fr(1, 1), 'gray64', pos)

    def draw(self, surface):
        super(Delta, self).draw(surface)
        surface.blit(self.rend, self.rend.get_rect(center=self.pos))


class AntiUp(Quark):
    def __init__(self, pos):
        super(AntiUp, self).__init__('anti-up', 'u', fr(-2, 3), 'dark red', pos, True)


class Hadron:
    def __init__(self, *quarks):
        self.quarks = quarks
        self.type = None
    
    @property
    def name(self):
        return self.type


class Baryon(Hadron):
    def __init__(self, quark1, quark2, quark3):
        super(Baryon, self).__init__(quark1, quark2, quark3)
        print(self.quarks)
        if num_of_type(self.quarks, Up) == 2 and num_of_type(self.quarks, Down):
            self.type = 'neutron'


class Desk:
    def __init__(self):
        self.surf = pygame.Surface((1270, 720))
        self.surf.fill('blue')


class Belt:
    def __init__(self):
        self.lines = []

    def new_line(self):
        self.lines.append(pygame.Rect(80, 560, 7, 110))

    def update(self):
        for entity in self.lines:
            entity.move_ip(4, 0)

        new_lines = self.lines[:]
        for num, line in enumerate(new_lines):
            if line.centerx > 1180:
                self.lines.pop(num)

    def draw(self, surface):
        pygame.draw.rect(surface, 'gray35', (90, 560, 1090, 110))
        for line in self.lines:
            pygame.draw.rect(surface, 'gray25', line)


class HadronMaker:
    def __init__(self):
        self.mode = 3
        self.angle = 0
        x, y = 425, 430
        self.size = 90
        ang = tau/3
        self.points = [(x + self.size * sin(ang * i), y + self.size * cos(ang * i)) for i in range(3)]
        self.slots = [None, None, None]
        self.active = False
        self.result = None

    def change_mode(self):
        if any(self.slots):
            return False
        if self.mode == 3:
            self.mode = 2
        elif self.mode == 2:
            self.mode = 3
        self.slots = [None]*self.mode

    def activate(self):
        if all(self.slots):
            self.active = True
        if not any(self.slots):
            self.change_mode()

    def update(self):
        if self.active:
            self.angle += 0.15
            self.size -= 0.3
            if self.size <= 1:
                self.active = False
                self.result = get_particle(*self.slots)
                for p in self.slots:
                    p.to_remove = True
                self.slots = [None]*len(self.slots)
                self.size = 90
                self.angle = 0
        x, y = 425, 430
        ang = tau/self.mode
        self.points = [(x + self.size * sin(ang * i + self.angle), y + self.size * cos(ang * i + self.angle)) for i in range(self.mode)]

    def draw(self, surface):
        pygame.draw.rect(surface, 'gray52', (300, 350, 350, 200))
        pygame.draw.circle(surface, 'gray31', (425, 430), 50)
        pygame.draw.line(surface, 'gray12', (425, 430), (425 + 150, 430), 3)
        for point in self.points:
            pygame.draw.line(surface, 'gray13', (425, 430), point, 8)
            pygame.draw.circle(surface, 'gray21', point, 19)
        pygame.draw.circle(surface, 'red', (425, 430), 25)
        pygame.draw.rect(surface, 'gray24', (560, 405, 50, 50))


class AntiMaker:
    def __init__(self):
        self.mode = 3
        self.angle = 0
        x, y = 800, 430
        self.size = 90
        ang = tau/3
        self.points = [800, 450 - 35]
        self.slot = None
        self.active = False
        self.result = None

    def activate(self):
        if self.slot is False:
            self.active = True

    def update(self):
        pass

    def draw(self, surface):
        x, y = 800, 450
        # pygame.draw.circle(surface, 'gray31', (800, 430), 50)
        # # pygame.draw.line(surface, 'gray12', (700, 430), (425 + 150, 430), 3)
        # for point in self.points:
        #     pygame.draw.line(surface, 'gray13', (800, 430), point, 8)
        #     pygame.draw.circle(surface, 'gray21', point, 19)
        # pygame.draw.circle(surface, 'red', (800, 430), 25)
        # pygame.draw.rect(surface, 'gray24', (560+300, 405, 50, 50))
        rect = pygame.Rect(0, 0, 100, 200)
        rect.center = x, y
        pygame.draw.rect(surface, 'gray31', rect)

        rect = pygame.Rect(0, 0, 50, 50)
        rect.center = x, y - 35
        pygame.draw.rect(surface, 'gray21', rect)
        # pygame.draw.line(surface, 'gray21', rect.bottomleft, (x, y + 35), 4)
        # pygame.draw.line(surface, 'gray21', rect.bottomright, (x, y + 35), 4)

        # rect = pygame.Rect(0, 0, 50, 50)
        # rect.center = x, y + 35
        # pygame.draw.rect(surface, 'gray21', rect)


class Customer:
    font = pygame.font.SysFont('arial', 23)

    def __init__(self, colour, level=0):
        self.pos = [random.randint(90, 1180), -30]
        self.desk_pos = (random.randint(90, 1180), 290)
        # self.pos = [295, 104]; self.desk_pos = (947, 297)
        self.direction = - atan2(self.pos[1] - self.desk_pos[1], self.pos[0] - self.desk_pos[0]) - tau/4
        self.colour = colour
        self.step = 0
        if level == 0:
            self.order = random.choice(('up', 'down'))
            self.enjoyment = random.randint(500, 900)
        elif level == 1:
            self.order = weighted_random(['up', 'down', 'strange', 'charm', 'top', 'bottom'], [10, 10, 6, 5, 1, 1])
            self.enjoyment = random.randint(500, 900)
        elif level == 2:
            self.order = weighted_random(['neutron', 'proton', 'up', 'down', 'strange', 'charm', 'top', 'bottom'], [5, 5, 4, 4, 5, 3, 2, 2])
            self.enjoyment = random.randint(900, 1000)
        elif level == 3:
            self.order = weighted_random(['neutron', 'proton', 'up', 'down', 'strange', 'charm', 'top', 'bottom'], [7, 7, 5, 5, 5, 5, 3, 3])
            self.enjoyment = random.randint(1000, 1200)
        elif level == 4:
            self.order = weighted_random(['neutron', 'proton', 'up', 'down', 'strange', 'charm', 'top', 'bottom'], [10, 10, 3, 3, 5, 5, 3, 3])
            self.enjoyment = random.randint(1000, 1400)
        else:
            self.order = weighted_random(['delta', 'sigma', 'xi', 'lambda', 'neutron', 'proton', 'up', 'down', 'strange', 'charm', 'top', 'bottom'], [4, 4, 3.5, 4, 7, 7, 3, 3, 5, 4, 2, 2])
            self.enjoyment = random.randint(1200, 2000)
        self.max_enj = self.enjoyment
        self.holding = None
        self.satisfaction = 0
        self.score_to_add = 0
        self.timer = 0

    def update(self):
        if self.step == 0:
            self.pos[0] += 3 * sin(self.direction)
            self.pos[1] += 3 * cos(self.direction)
            if self.pos[1] > 290:
                self.step = 1
        if self.step == 1:
            CUSTOMERS.append(self)
            self.step = 2
        if self.step == 2:
            self.enjoyment -= 1
            if self.enjoyment < 0:
                self.step = 3
            if self.holding is not None:
                self.step = 3
        if self.step == 3:
            self.pos[1] -= 3
            if self.pos[1] < -35:
                self.step = 4
        if self.step == 4:
            if self.holding is None:
                self.satisfaction = 0
                return None
            if self.order == self.holding.name:
                if self.order in ('up', 'down'):
                    self.score_to_add += 20
                if self.order in ('charm', 'strange', 'top', 'bottom'):
                    self.score_to_add += 50
                if self.order in ('neutron', 'proton'):
                    self.score_to_add += 100
                if self.order in ('lambda', 'xi', 'sigma', 'delta'):
                    self.score_to_add += 200
            self.satisfaction = self.score_to_add
            self.step = 5
        if self.step == 5:
            self.timer += 1
            if self.timer > 50:
                self.step = 6

    def draw_anger_bar(self, surface):
        x, y = self.pos
        # score_rend = self.font.render(str(round(self.enjoyment/self.max_enj, 2)), True, (0, 0, 0))
        # surface.blit(score_rend, score_rend.get_rect(center=(self.pos[0] + 50, self.pos[1])))
        pygame.draw.rect(surface, 'gray100', (x + 40, y - 25 + 50*((self.max_enj-self.enjoyment)/self.max_enj), 15, 50*(self.enjoyment/self.max_enj)))
        pygame.draw.rect(surface, 'gray12', (x + 40, y - 25, 15, 50), 4)

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos, 20)
        self.draw_anger_bar(surface)
        if self.step == 2:
            x, y = self.pos
            pygame.draw.line(surface, 'black', (x + 25, y - 25), (x + 50, y - 50), 5)
            pygame.draw.rect(surface, 'white', (x + 10, y - 140, 160, 80))
            pygame.draw.rect(surface, 'gray37', (x + 10, y - 140, 160, 80), 3)
            if self.order == 'up':
                rend = self.font.render(f"I would like an ", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 130))
                rend = self.font.render(f"up quark", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 101))
            elif self.order in ('up', 'down', 'top', 'bottom', 'strange', 'charm'):
                rend = self.font.render(f"I would like a ", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 130))
                rend = self.font.render(f"{self.order} quark", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 101))
            elif self.order in ('proton', 'neutron'):
                rend = self.font.render(f"I would like a ", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 130))
                rend = self.font.render(f"{self.order} particle", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 101))
            else:
                rend = self.font.render(f"I would like a ", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 130))
                rend = self.font.render(f"{self.order} particle", True, (0, 0, 0))
                surface.blit(rend, (x + 25, y - 101))

        if self.step == 5:
            global creds
            x, y = self.pos
            pygame.draw.line(surface, 'black', (x, y + 50), (x, y + 90), 5)
            rend = self.font.render(f"{self.satisfaction} creds", True, (0, 0, 0))
            creds += self.score_to_add
            self.score_to_add = 0
            surface.blit(rend, rend.get_rect(center=(x, y + 130)))


class Displaying:
    def __init__(self, quark):
        self.quark = quark
        self.active = False
        self.font = pygame.font.SysFont('arial', 23)

    def set_quark(self, new_quark):
        self.quark = new_quark
        self.active = True

    def draw(self, surface):
        if self.active:
            if distance(self.quark.pos, pygame.mouse.get_pos()) > 50:
                self.active = False
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(surface, 'gray32', (x, y, 140, 120))
            TextBox((x+15, y+15), f"name: {self.quark.name}", 23).draw(surface)
            TextBox((x+15, y+40), f"symbol: {self.quark.symbol}", 23).draw(surface)
            TextBox((x+15, y+65), f"charge: {self.quark.charge}e", 23).draw(surface)


def distance(p1, p2):
    return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), 0.5)


def wait_for_click():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    running = False


def start_text(surface):
    surface.fill('gray')
    t = TextBox((100, 100), 'The goal of this game is to create hadrons for the customers\nA hadron is a particle/antiparticle affected by the strong nuclear force\nThere are 2 types of hadron\nBaryons are made from the combination of 3 quarks\nMesons are made of the combinations of 2 quarks\n\n\nClick to continue', 40)
    t.draw(surface)
    pygame.display.update()
    wait_for_click()


def text1(surface):
    surface.fill('gray')
    t = TextBox((100, 100), 'A Lepton is a type of fundament particle that is not\naffected by the strong nuclear force\nexamples of these are electrons and neutrinos', 40)
    t.draw(surface)
    pygame.display.update()
    wait_for_click()


def text2(surface):
    surface.fill('gray')
    t = TextBox((100, 100), 'In 1964 Murray Gell-Mann first postulated the existence of quarks.\nQuarks are a group of fundamental particles that make up hadrons\nThe evidence for the existence of fundament particles\ncomes from experiments preformed in particle accelerators\nwhere non fundamental particles are broken apart', 40)
    t.draw(surface)
    pygame.display.update()
    wait_for_click()


def text3(surface):
    surface.fill('gray')
    t = TextBox((100, 100), "Quarks have spin and charge\nthe charge of a Quark is measured\nas a fraction of the elementary charge 'e'\nThe charge of an anti-quark is the opposite\nof the charge of its counterpart", 40)
    t.draw(surface)
    pygame.display.update()
    wait_for_click()


def text4(surface):
    surface.fill('gray')
    t = TextBox((100, 100), "", 40)
    t.draw(surface)
    pygame.display.update()
    wait_for_click()


def weighted_random(seq, chance):
    total = sum(chance)
    rand = random.random() * total
    for i, v in zip(seq, chance):
        rand -= v
        if rand <= 0:
            return i
        
        
def num_of_type(seq, type_):
    return len([None for i in seq if isinstance(i, type_) or i == type_])


def check_blocks(blocks, seq):
    for type_ in ALL_QUARKS:
        if num_of_type(blocks, type_) != num_of_type(seq, type_):
            return False
    return True


def get_particle(*blocks):
    pos = 585, 430
    if len(blocks) == 3:
        if check_blocks(blocks, [Up, Down, Down]):
            return Neutron(pos)
        if check_blocks(blocks, [Up, Up, Down]):
            return Proton(pos)
        if check_blocks(blocks, [Up, Down, Strange]):
            return Lambda(pos)
        if check_blocks(blocks, [Up, Up, Strange]) or check_blocks(blocks, [Up, Down, Strange]) or check_blocks(blocks, [Down, Down, Strange]):
            return Sigma(pos)
        if check_blocks(blocks, [Up, Strange, Strange]) or check_blocks(blocks, [Down, Strange, Strange]):
            return Xi(pos)
        if check_blocks(blocks, [Up, Up, Up]) or check_blocks(blocks, [Down, Down, Down]):
            return Delta(pos)


ALL_QUARKS = [Up, Down, Strange, Charm, Top, Bottom]

MENU_FONT = pygame.font.SysFont('arial', 30)

FPS = 60

NEW_LINE = USEREVENT + 1
pygame.time.set_timer(NEW_LINE, 1000)
CUSTOMERS = []


NEW_QUARK = USEREVENT + 2
pygame.time.set_timer(NEW_QUARK, 1500)

NEXT_CUSTOMER = USEREVENT + 3
pygame.time.set_timer(NEXT_CUSTOMER, 8000)

LEVEL_UP = USEREVENT + 4
pygame.time.set_timer(LEVEL_UP, 30000)

POINTS = (((65.0, 395.0), (65.0, 465.0)),
          ((135.0, 395.0), (135.0, 465.0)),
          ((205.0, 395.0), (205.0, 465.0)))
BOX = [[None, None], [None, None], [None, None]]

hm = HadronMaker()
am = AntiMaker()
dsp = Displaying(None)
creds = 0


def main():
    global hm
    fps = pygame.time.Clock()

    screen = pygame.display.set_mode((1270, 720))
    pygame.display.set_caption("FUNdamental")

    start_text(screen)
    text1(screen)
    text2(screen)
    text3(screen)

    picked_up = None
    belt = Belt()
    quarks = []
    c1 = Customer('red')
    customers = [c1]
    level = 0
    running = True
    while running:
        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                print(event.pos)
                if event.button == 3:
                    for quark in quarks:
                        if distance(event.pos, quark.pos) < 30:
                            dsp.set_quark(quark)

                if event.button == 1:
                    if distance(event.pos, (425, 430)) < 40:
                        hm.activate()
                    if picked_up is not None:
                        if picked_up.put_down(event.pos):
                            picked_up = None
                        continue
                    for quark in quarks:
                        if distance(event.pos, quark.pos) < 30:
                            quark.picked_up = True
                            if quark.box_pos is not None:
                                BOX[quark.box_pos[0]][quark.box_pos[1]] = None
                                quark.box_pos = None
                            if quark.maker_index is not None:
                                if hm.active:
                                    break
                                hm.slots[quark.maker_index] = None
                                quark.maker_index = None
                            if quark.am is not None:
                                am.slot = None
                                quark.am = None
                            picked_up = quark
                            break
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    hm.change_mode()

            if event.type == NEW_LINE:
                belt.new_line()
            if event.type == NEW_QUARK:
                quarks.append(weighted_random(ALL_QUARKS, [10, 10, 5, 4, 2, 2])((45, 615)))
            if event.type == NEXT_CUSTOMER:
                customers.append(Customer('green', level))
            if event.type == LEVEL_UP:
                level += 1

        # update
        belt.update()
        for entity in quarks:
            entity.update()
        for num, quark in enumerate(quarks):
            if quark.pos[0] > 1220 and picked_up is None:
                quark.to_remove = True
        quarks = [q for q in quarks if not q.to_remove]
        for entity in customers:
            entity.update()
        hm.update()
        am.update()
        if hm.result is not None:
            quarks.append(hm.result)
            hm.result = None

        # draw
        screen.fill('gray57')
        pygame.draw.rect(screen, 'gray42', (0, 330, 1270, 720))

        for entity in customers:
            entity.draw(screen)

        belt.draw(screen)
        hm.draw(screen)
        # am.draw(screen)

        size = 70
        pygame.draw.rect(screen, '#F4E2C6', (30, 360, size * 3, size * 2))
        for x in range(3):
            for y in range(2):
                pygame.draw.circle(screen, '#A9957B', (x*size + 30 + size/2, y*size + 360 + size/2), 25)

        for entity in quarks:
            entity.draw(screen)

        pygame.draw.rect(screen, 'gray17', (15, 540, 75, 150))

        rend = MENU_FONT.render(str(creds), True, (0, 0, 0))
        screen.blit(rend, rend.get_rect(top=0, right=1270))

        dsp.draw(screen)

        pygame.display.update()
        fps.tick(FPS)


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
