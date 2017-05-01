
"""
Conway's Game of Life
The "game" is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.
At each step in time, the following transitions occur:
1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

import pygame, sys, time
import numpy as np
from pygame.locals import *

#The WIDTH and HEIGHT of the game
WIDTH = 80
HEIGHT = 40

#The global vairable for detecting the click button
pygame.button_down = False

# The world map
pygame.world=np.zeros((HEIGHT,WIDTH))

# Draw cell
class Cell(pygame.sprite.Sprite):
    
    size = 10

    def __init__(self, position):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([self.size, self.size])

        # fill white
        self.image.fill((255,255,255))

        # ����һ�������Ͻ�Ϊê��ľ���
        self.rect = self.image.get_rect()
        self.rect.topleft = position

#��ͼ������ע�⵽�����ǰѻ����������ٱ������������ͼ������кܴ�����������ռ�
def draw():
    screen.fill((0,0,0))
    for sp_col in range(pygame.world.shape[1]):
        for sp_row in range(pygame.world.shape[0]):
            if pygame.world[sp_row][sp_col]:
                new_cell = Cell((sp_col * Cell.size,sp_row * Cell.size))
                screen.blit(new_cell.image,new_cell.rect)
                
#����ϸ�����¹�����µ�ͼ
def next_generation():
    nbrs_count = sum(np.roll(np.roll(pygame.world, i, 0), j, 1)
                 for i in (-1, 0, 1) for j in (-1, 0, 1)
                 if (i != 0 or j != 0))

    pygame.world = (nbrs_count == 3) | ((pygame.world == 1) & (nbrs_count == 2)).astype('int')

#��ͼ��ʼ��
def init():
    pygame.world.fill(0)
    draw()
    return 'Stop'

#ֹͣʱ�Ĳ���
def stop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN and event.key == K_RETURN:
            return 'Move'
        
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'

        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button
        
        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1: #������
                pygame.world[sp_row][sp_col] = 1
            elif pygame.button_type == 3: #����Ҽ�
                pygame.world[sp_row][sp_col] = 0
            draw()

    return 'Stop'

#��ʱ��������֡��
pygame.clock_start = 0


#�����ݻ�ʱ�Ĳ���
def move():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            return 'Stop'
        if event.type == KEYDOWN and event.key == K_r:
            return 'Reset'
        if event.type == MOUSEBUTTONDOWN:
            pygame.button_down = True
            pygame.button_type = event.button
        
        if event.type == MOUSEBUTTONUP:
            pygame.button_down = False

        if pygame.button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_col = mouse_x / Cell.size;
            sp_row = mouse_y / Cell.size;

            if pygame.button_type == 1:
                pygame.world[sp_row][sp_col] = 1
            elif pygame.button_type == 3:
                pygame.world[sp_row][sp_col] = 0
            draw()

        
    if time.clock() - pygame.clock_start > 0.02:
        next_generation()
        draw()
        pygame.clock_start = time.clock()

    return 'Move'



if __name__ == '__main__':

    #״̬����Ӧ����״̬����ʼ����ֹͣ������
    state_actions = {
            'Reset': init,
            'Stop': stop,
            'Move': move
        }
    state = 'Reset'

    pygame.init()
    pygame.display.set_caption('Conway\'s Game of Life')

    screen = pygame.display.set_mode((WIDTH * Cell.size, HEIGHT * Cell.size))
    
    while True: # ��Ϸ��ѭ��

        state = state_actions[state]()
        pygame.display.update()