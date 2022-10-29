import pygame, sys
from pygame import Vector2
import math

FPS = 60

WIDTH = 600
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 1)
clock = pygame.time.Clock()

def dot(center, color = 'white'):
    pygame.draw.circle(screen, color, center, 1)

def line(st_pos, end_pos, color = 'white'):
    pygame.draw.line(screen, color, st_pos, end_pos, 3)

def top_rot_line(D, d, angle):
    x = D * math.cos(math.radians(angle)) + (WIDTH/2)
    y = -d * math.sin(math.radians(angle)) + ((HEIGHT/2) - 120)

    return (x, y)

def bot_rot_line(D, d, angle):
    x = D * math.cos(math.radians(angle)) + (WIDTH/2)
    y = -d * math.sin(math.radians(angle)) + ((HEIGHT/2) + 120)

    return (x, y)

class Cube():
    def __init__(self, big_diamiter, small_diamiter, center):
        self.D = big_diamiter
        self.d = small_diamiter
        self.c = center
        self.t = 0

    def render(self):
        top_p1 = top_rot_line(self.D, self.d, self.t + 0)
        bot_p1 = bot_rot_line(self.D, self.d, self.t + 0)

        top_p2 = top_rot_line(self.D, self.d, self.t + 90)
        bot_p2 = bot_rot_line(self.D, self.d, self.t + 90)
        line(top_p2, bot_p2)

        top_p3 = top_rot_line(self.D, self.d, self.t + 180)
        bot_p3 = bot_rot_line(self.D, self.d, self.t + 180)
        line(top_p3, bot_p3)

        top_p4 = top_rot_line(self.D, self.d, self.t + 270)
        bot_p4= bot_rot_line(self.D, self.d, self.t + 270)
        line(top_p4, bot_p4)

        line(bot_p1, bot_p2)
        line(bot_p2, bot_p3)
        line(bot_p3, bot_p4)
        line(top_p1, bot_p1, 'red')
        line(bot_p4, bot_p1)

        line(top_p1, top_p2)
        line(top_p2, top_p3)
        line(top_p3, top_p4)
        line(top_p4, top_p1)

class Triangle():
    def __init__(self, big_diamiter, small_diamiter, center):
        self.c = center
        self.t = 0
        self.D = big_diamiter
        self.d = small_diamiter

    def render(self):
        top_p = (WIDTH/2, 180)

        bot_p1 = bot_rot_line(self.D, self.d, (self.t + 0))
        bot_p2 = bot_rot_line(self.D, self.d, (self.t + 90))
        bot_p3 = bot_rot_line(self.D, self.d, (self.t + 180))
        bot_p4 = bot_rot_line(self.D, self.d, (self.t + 270))

        line(top_p, bot_p1, 'red')
        line(top_p, bot_p2)
        line(top_p, bot_p3)
        line(top_p, bot_p4)

        line(bot_p1, bot_p2)
        line(bot_p2, bot_p3)
        line(bot_p3, bot_p4)
        line(bot_p4, bot_p1)
 
cube = Cube(200, 25, Vector2((WIDTH/2, HEIGHT/2)))
triangle = Triangle(200, 25, Vector2((WIDTH/2, HEIGHT/2)))

while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            # triangle.t += 0.1
            cube.t += 0.01


    screen.fill((25, 25, 25))
    # triangle.render()
    cube.render()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cube.t += 0.9

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cube.t -= 2

    pygame.display.flip()
    clock.tick(FPS)