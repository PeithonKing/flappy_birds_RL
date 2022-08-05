import pygame
from simple_pid import PID
import time
from random import randint


# initialize pygame
pygame.init()

disp_x, disp_y = 800, 600
# create the screen
screen = pygame.display.set_mode((disp_x, disp_y))

# defining various colors
white = "#ffffff"
green = "#00ff00"
blue = "#0000ff"
black = "#000000"
red = "#ff0000"
violet = "#ff00ff"
custom_violet = "#8f00ff"

# obj_pos = (randint(0, disp_x), randint(0, disp_y))
# tar_pos = (randint(0, disp_x), randint(0, disp_y))

obj_pos = (100, 100)
tar_pos = (disp_x/2, disp_y/2)

Kp = 10/100
Kd = 0/100
Ki = 5/100
pid_x = PID(Kp, Ki, -Kd, setpoint=tar_pos[0], sample_time=0.1)
pid_y = PID(Kp, Ki, -Kd, setpoint=tar_pos[1], sample_time=0.1)

# game loop
running = True
while running:
    screen.fill(custom_violet) # violet
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    # targer circle
    pygame.draw.circle(screen, red, (tar_pos[0], tar_pos[1]), 20, 0)
    
    # moving Circle
    control_x = pid_x(obj_pos[0])
    control_y = pid_y(obj_pos[1])
    
    obj_pos = (obj_pos[0] + control_x, obj_pos[1] + control_y)
    # print(obj_pos)
    
    pygame.draw.circle(screen, green, obj_pos, 19, 3)
    
    pygame.display.update()
    
    time.sleep(0.1)