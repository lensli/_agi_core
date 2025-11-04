import random,time
import pygame

from lib.shape_group import ponits_update
pygame.init()
screen  = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()
run_ctrl = True


all_point = []
while run_ctrl:
    for ecent in pygame.event.get():
        if ecent.type == pygame.QUIT:
            run_ctrl = False
    mouse_pose = pygame.mouse.get_pos()
    screen.fill("purple")
    all_point = ponits_update(all_point,mouse_pose)
    for p in all_point:
        screen.set_at((p.x,p.y),p.color)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
