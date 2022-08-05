from re import S
import pygame
import time
from random import randint


# initialize pygame
pygame.init()
disp_x, disp_y = 500, 700
# create the screen
screen = pygame.display.set_mode((disp_x, disp_y))
clock = pygame.time.Clock()

# defining various colors
white = "#ffffff"
green = "#00ff00"
dark_green = "#007700"
blue = "#0000ff"
black = "#000000"
red = "#ff0000"
violet = "#ff00ff"
custom_violet = "#8f00ff"

g = 1100  # pixel/s2  # acceleration due to gravity
fps = 100  # frames per second
damp = 0.8  # damping factor on collision with bouncing surfaces

class Bird:
    def __init__(self, key, colour=red, radius=20, border=5, x = 100, reward = 0):
        self.key = key
        self.colour = colour
        self.radius = radius
        self.border = border
        self.x = x
        self.reward = reward
        self.alive = True
        self.s0 = disp_y/2  # default position of the bird
        self.v0 = 0  # 650  # default velocity of the bird
        # print(self.v0)
        self.jump_height = 350  # jump height
        self.s = self.s0
        self.v = self.v0
        
    def draw(self, screen = screen):
        if self.alive:
            self.bird_pos_after(dt)
            pygame.draw.circle(screen, self.colour, (self.x, disp_y-self.s), self.radius, self.border)

    def bird_pos_after(self, dt):
        # print(f"dt = {dt}")
        s = self.s
        v = self.v
        s += self.v*dt - g*dt**2/2
        v -= g*dt
        if s <= self.radius:
            s = self.radius-1
            v = -v*damp
        elif s >= disp_y-self.radius:
            s = disp_y-self.radius
            v = -v*damp
        self.s = s
        self.v = v
    
    def jump(self, key = None):
        if not key or key == self.key:
            self.v += self.jump_height
    
    def kill(self):
        self.reward -= 150
        self.alive = False


class Obstacle:
    def __init__(self, gap = 200, length=200):
        self.gap = gap
        self.length = length
        self.x = disp_x
        self.gap_y = randint(self.gap/2+25, disp_y-self.gap/2-25)
        self.colour = dark_green
        self.speed = 200
        
    def draw(self, screen = screen):
        # [left, top, width, height]
        pygame.draw.rect(screen, self.colour, (self.x, 0, self.length, self.gap_y-self.gap/2))
        pygame.draw.rect(screen, self.colour, (self.x, self.gap_y+self.gap/2, self.length, disp_y-self.gap_y-self.gap/2))
        self.x -= self.speed*dt
        if self.x < 100-self.length:
            reward()
            self.x = disp_x
            self.gap_y = randint(self.gap/2+25, disp_y-self.gap/2-25)

def collide(bird, o):
    if o.x>bird.x:
        return False
    elif o.gap_y-o.gap/2 < disp_y-bird.s < o.gap_y+o.gap/2:
        # print(f"{o.gap_y-o.gap/2} < {disp_y-bird.s} < {o.gap_y+o.gap/2}")
        return False
    else:
        # print(f"{o.gap_y-o.gap/2} not < {disp_y-bird.s} not < {o.gap_y+o.gap/2}")
        print("kill a bird!")
        return True

def reward():
    give = 100
    for bird in birds:
        if bird.alive:
            bird.reward += give
        print(f"{bird.key} reward = {bird.reward},", end=" ")
    print()

birds = [
    Bird(key = pygame.K_a),
    Bird(key = pygame.K_s, colour=green)
    ]

birds_alive = len(birds)

running = True
t0 = time.time()
frame_count = 0

obstacle = Obstacle()

# 

# game loop
while running and birds_alive:
    dt = clock.tick(100)/1000
    frame_count += 1
    screen.fill(black)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for bird in birds:
                if bird.alive:
                    bird.jump(event.key)
    
    obstacle.draw()

    for bird in birds:
        if bird.alive:
            bird.draw()
    
    # kill bird if it hits the obstacle
    for bird in birds:
        if bird.alive:
            if collide(bird, obstacle):
                bird.kill()
                birds_alive -= 1
    
    pygame.display.update()

# conclusion
screen.fill(black)
obstacle.draw()
pygame.display.update()
for bird in birds:
    print(f"{bird.key} reward = {bird.reward},", end=" ")
time.sleep(0.5)

print(f"\nfps = {frame_count/(time.time()-t0)}")