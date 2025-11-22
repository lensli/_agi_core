import random,time
import pygame

from lib.shape_group import ponits_update
pygame.init()
screen  = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()
run_ctrl = True

hm_regular_ttf_path = os.path.join(CURRENTDIR,"dlm_lib","lib_res","front","HarmonyOS_Sans_SC_Regular.ttf")


all_point = []
while run_ctrl:
    fps_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_ctrl = False

    mouse_pose = pygame.mouse.get_pos()
    screen.fill("purple")
    all_point = ponits_update(all_point,mouse_pose)
    for p in all_point:
        screen.set_at((p.x,p.y),p.color)
    pygame.display.flip()
    print(f"fps:{1/(time.time()-fps_time)}")
    # clock.tick(60)
pygame.quit()
