import pygame, sys, os
from pygame import Vector2
import math
import cv2
import numpy as np

FPS = 60

WIDTH = 600
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CUBE')
icon = pygame.image.load('icon.png').convert_alpha()
pygame.display.set_icon(icon)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 1)
clock = pygame.time.Clock()
colors = ['red', 'green', 'blue', 'yellow']


def dot(center, color = 'white'):
    pygame.draw.circle(screen, color, center, 1)

def line(st_pos, end_pos, color = 'white', width = 3):
    pygame.draw.line(screen, color, st_pos, end_pos, width)

def top_rot_line(D, d, angle):
    x = D * math.cos(math.radians(angle)) + (WIDTH/2)
    y = -d * math.sin(math.radians(angle)) + ((HEIGHT/2) - 120)

    return (x, y)

def bot_rot_line(D, d, angle):
    x = D * math.cos(math.radians(angle)) + (WIDTH/2)
    y = -d * math.sin(math.radians(angle)) + ((HEIGHT/2) + 120)
    return (x, y)

def line_len(p1, p2):
    return math.sqrt(pow((p2.x - p1.x), 2) + pow((p2.y - p1.y), 2))

def lerp(p0, p1, t):
    return p0 + t * (p1 - p0)

def bubble_sort(y_list, x_list):
    sorted_list = [[None, None], [None, None], [None, None], [None, None]]
    temp_y = None
    temp_x = None

    for i in range(0, len(y_list)):
        for j in range(i, len(y_list)):
            if y_list[j] < y_list[i]:
                temp_y = y_list[i]
                temp_x = x_list[i]
                x_list[i] = x_list[j]
                y_list[i] = y_list[j]
                y_list[j] = temp_y
                x_list[j] = temp_x

    sorted_list = list()
    for i in range(0, len(x_list)):
        sorted_list.append([x_list[i], y_list[i]])

    return sorted_list


class Cube():
    def __init__(self, big_diamiter, small_diamiter, center):
        self.D = big_diamiter
        self.d = small_diamiter
        self.c = center
        self.t = 10
        self.img_count = 0
        self.imgs_paths = ['.\\img\\' + file_name for file_name in os.listdir('.\\img\\')]
        self.img_path = self.imgs_paths[0]
        self.img = cv2.imread(self.img_path)
        self.img_width = self.img.shape[1]
        self.img_height = self.img.shape[0]

    def img_update(self):
        self.img_count += 1
        if self.img_count > (len(self.imgs_paths)-1):
            self.img_count = 0
        self.img_path = self.imgs_paths[self.img_count]
        self.img = cv2.imread(self.img_path)
        self.img_width = self.img.shape[1]
        self.img_height = self.img.shape[0]

    def render(self):

        top_p1 = top_rot_line(self.D, self.d, self.t + 0)
        bot_p1 = bot_rot_line(self.D, self.d, self.t + 0)
        # line(top_p1, bot_p1, 'red')

        top_p2 = top_rot_line(self.D, self.d, self.t + 90)
        bot_p2 = bot_rot_line(self.D, self.d, self.t + 90)
        # line(top_p2, bot_p2, 'blue')

        top_p3 = top_rot_line(self.D, self.d, self.t + 180)
        bot_p3 = bot_rot_line(self.D, self.d, self.t + 180)
        # line(top_p3, bot_p3, 'green')

        top_p4 = top_rot_line(self.D, self.d, self.t + 270)
        bot_p4= bot_rot_line(self.D, self.d, self.t + 270)
        # line(top_p4, bot_p4, 'yellow')

        all_top_points_y = [top_p1[1], top_p2[1], top_p3[1], top_p4[1]]
        all_top_points_x = [top_p1[0], top_p2[0], top_p3[0], top_p4[0]]

        all_top_points = bubble_sort(all_top_points_y, all_top_points_x)

        all_bot_points_y = [bot_p1[1], bot_p2[1], bot_p3[1], bot_p4[1]]
        all_bot_points_x = [bot_p1[0], bot_p2[0], bot_p3[0], bot_p4[0]]

        all_bot_points = bubble_sort(all_bot_points_y, all_bot_points_x)

        self.render_img(all_top_points[0], all_top_points[1], all_bot_points[0], all_bot_points[1])
        self.render_img(all_top_points[2], all_top_points[0], all_bot_points[2], all_bot_points[0])
        self.render_img(top_p1, top_p2, top_p4, top_p3)
        self.render_img(bot_p1, bot_p2, bot_p4, bot_p3)
        self.render_img(all_top_points[3], all_top_points[1], all_bot_points[3], all_bot_points[1])
        self.render_img(all_top_points[2], all_top_points[3], all_bot_points[2], all_bot_points[3])


    def render_img(self, top_left_p, top_right_p, bot_left_p, bot_right_p):

        input_points = np.float32([[0, 0], [self.img_width, 0], [0, self.img_height], [self.img_width, self.img_height]])
        output_points = np.float32([top_left_p, top_right_p, bot_left_p, bot_right_p])

        matrix = cv2.getPerspectiveTransform(input_points, output_points)
        img_output = cv2.warpPerspective(self.img.copy(), matrix, (WIDTH, HEIGHT))

        cv2.imwrite('rotating-cube-img.png', img_output)

        pygame_img = pygame.image.load('rotating-cube-img.png')
        pygame_img.set_colorkey((0, 0, 0))
        screen.blit(pygame_img, (0, 0))

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

        line(top_p, bot_p1)
        line(top_p, bot_p2)
        line(top_p, bot_p3)
        line(top_p, bot_p4)

        line(bot_p1, bot_p2, 'red')
        line(bot_p2, bot_p3)
        line(bot_p3, bot_p4)
        line(bot_p4, bot_p1)

        self.render_img(top_p, bot_p2, bot_p1)

    def render_img(self, top_p, bot_left_p, bot_right_p):

        input_points = np.float32([[0, 0], [self.img_width, 0], [0, self.img_height], [self.img_width, self.img_height]])
        output_points = np.float32([[top_p[0]-1, top_p[1]], [top_p[0]+1, top_p[1]], bot_left_p, bot_right_p])

        matrix = cv2.getPerspectiveTransform(input_points, output_points)
        img_output = cv2.warpPerspective(self.img.copy(), matrix, (WIDTH, HEIGHT))

        cv2.imwrite('rotating-triangle-img.png', img_output)

        pygame_img = pygame.image.load('rotating-triangle-img.png')
        pygame_img.set_colorkey((0, 0, 0))
        screen.blit(pygame_img, (0, 0))

class Text():
    def __init__(self, center_pos, txt, size, color = 'white', bg_color = 'black', antialias = True, font = 'arial'):
        self.txt = txt
        self.color = color
        self.bg_color = bg_color
        self.antialias = antialias
        self.center_pos = center_pos
        self.font = pygame.font.SysFont(font, size)
        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)

    def render(self):
        screen.blit(self.rendered_txt, self.rect)

    def update(self, new_txt = None, new_center = None, new_color = None, new_bg_color = None):
        if new_txt == None:
            new_txt = self.txt
        else:
            self.txt = new_txt

        if new_center == None:
            new_center = self.center_pos
        else:
            self.center_pos = new_center

        if new_color == None:
            new_color = self.color
        else:
            self.color = new_color

        if new_bg_color == None:
            new_bg_color = self.bg_color
        else:
            self.bg_color = new_bg_color

        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)
 
cube = Cube(200, 25, Vector2((WIDTH/2, HEIGHT/2)))
triangle = Triangle(200, 25, Vector2((WIDTH/2, HEIGHT/2)))

render_cube = True

cube_name = Text((WIDTH/2, 50), (cube.img_path.replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('.\img\\', '') + '-cube').upper(), 50, bg_color=None)

while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            triangle.t += 0.01
            cube.t += 0.01

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cube.img_update()
                cube_name.update((cube.img_path.replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('.\img\\', '') + '-cube').upper())

    screen.fill((25, 25, 25))

    cube.render() if render_cube else triangle.render()

    cube_name.render()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cube.t += 1
        triangle.t += 1

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cube.t -= 2
        triangle.t -= 2

    pygame.display.flip()
    clock.tick(FPS)