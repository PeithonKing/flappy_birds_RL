import pygame
# import time
from random import randint


# initialize pygame
pygame.init()
disp_x, disp_y = 500, 700
g = 1100   # pixel/s2  # acceleration due to gravity

# defining various colors
# white = "#ffffff"
# green = "#00ff00"
dark_green = "#007700"
# blue = "#0000ff"
black = "#000000"
red = "#ff0000"
# violet = "#ff00ff"
# custom_violet = "#8f00ff"


class Bird:
    def __init__(self, key=None, colour=red, radius=20, border=5, x = 100, damp = 0.8):
        self.key = key
        self.colour = colour
        self.radius = radius
        self.border = border
        self.x = x
        self.damp = damp
        self.g = g
        # self.reward = reward  # 0
        self.alive = True
        self.s0 = disp_y/2  # default position of the bird
        self.v0 = 0  # 650  # default velocity of the bird
        # print(self.v0)
        self.jump_height = 500  # jump height
        self.s = self.s0
        self.v = self.v0
        
    def draw(self, screen, dt):
        if self.alive:
            self.bird_pos_after(dt)
            pygame.draw.circle(screen, self.colour, (self.x, self.s), self.radius, self.border)

    def bird_pos_after(self, dt):
        # print(f"dt = {dt}")
        s = self.s
        v = self.v
        s += self.v*dt + self.g*dt**2/2
        v += self.g*dt
        # if s <= self.radius:  # collides with the ground
        #     # print("collides with the ground")
        #     s = self.radius-1
        #     v = -v*self.damp
        # elif s >= disp_y-self.radius:  # collides with the ceiling
        #     # print("collides with the ceiling")
        #     s = disp_y-self.radius
        #     v = -v*self.damp
        # print(f"\t{self.s} | {self.v} | {s} | {v} | {self.g*dt} | {dt}")
        self.s = s
        self.v = v
    
    def jump(self):
        self.v -= self.jump_height
    
    def kill(self):
        # self.reward -= 150
        self.alive = False


class Obstacle:
    def __init__(self, gap = 150, length=200):
        self.gap = gap
        self.length = length
        self.x = disp_x
        self.gap_y = randint(self.gap/2+25, disp_y-self.gap/2-25)
        self.colour = dark_green
        self.speed = 200
        
    def draw(self, screen, dt):
        # [left, top, width, height]
        pygame.draw.rect(screen, self.colour, (self.x, 0, self.length, self.gap_y-self.gap/2))
        pygame.draw.rect(screen, self.colour, (self.x, self.gap_y+self.gap/2, self.length, disp_y-self.gap_y-self.gap/2))
        self.x -= self.speed*dt
        if self.x < 100-self.length:
            self.x = disp_x
            self.gap_y = randint(self.gap/2+25, disp_y-self.gap/2-25)
            return True  # score for passing an obstacle
        return False


class FlappyBird:
    def __init__(self, disp_x=disp_x, disp_y=disp_y):
        self.disp_x = disp_x
        self.disp_y = disp_y
        # init display
        self.screen = pygame.display.set_mode((disp_x, disp_y))
        self.clock = pygame.time.Clock()
        self.g = g
        self.fps = 100  # frames per second
        self.damp = 0.8  # damping factor on collision with bouncing surfaces
        pygame.display.set_caption('Flappy Birds!')
        self.reset()
    
    def reset(self):
        self.birds = [
            Bird(key = pygame.K_a),
            # Bird(key = pygame.K_s, colour=green)
            ]
        self.birds_alive = len(self.birds)
        self.obstacle = Obstacle()
        self.score = 0

    def collide(self, bird, o):
        if o.x>bird.x:  # obstacle is to the right of the bird
            return False
        elif o.gap_y-o.gap/2 < bird.s < o.gap_y+o.gap/2:
            # print(f"{o.gap_y-o.gap/2} < {disp_y-bird.s} < {o.gap_y+o.gap/2}")
            return False
        else:
            # print(f"{o.gap_y-o.gap/2} not < {disp_y-bird.s} not < {o.gap_y+o.gap/2}")
            # print("kill a bird!")
            return True
        
    def reward(self, bird, obstacle):
        return int((disp_y/4 -abs(bird.s-obstacle.gap_y)))
    
    def play_step(self, actions, events = None):
        # actions = [[0, 1] or [1, 0]]*len(self.birds)  # which is fortunately 1 here
        # [1, 0] = jump
        # [0, 1] = do nothing
        success = False
        # collect user input, create background and clock ticks
        dt = self.clock.tick(100)/1000
        self.screen.fill(black)
        if events == None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # pygame.quit()
                # quit()
                return 0, True, self.score
        
        # render characters
        if self.obstacle.draw(self.screen, dt):
            self.score += 1
            success = True
        for bird in self.birds:
            if bird.alive:
                bird.draw(self.screen, dt)
        
        # jump bird if needed
        for i in range(len(self.birds)):
            if self.birds[i].alive and actions[i][0]:
                self.birds[i].jump()

        # kill bird if it hits the obstacle
        for bird in self.birds:
            if bird.alive:
                collided = self.collide(bird, self.obstacle)
                reward = self.reward(bird, self.obstacle)
                if collided:
                    bird.kill()
                    self.birds_alive -= 1
                    reward = -10
        
        # update the screen
        pygame.display.update()
        if success:
            reward = 10
        # return reward, game_over, score
        # print(reward)
        return reward, self.birds_alive == 0, self.score
              # int      bool       int

if __name__ == "__main__":
    game = FlappyBird(disp_x, disp_y)
    
    game_over = False
    score = 0
    total_reward = 0
    while not game_over:
        action = [0, 1]
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("jump")
                    action = [1, 0]
                
        reward, game_over, new_score = game.play_step([action], events)
        if score != new_score:
            print(f"score = {new_score}")
        if reward:
            total_reward += reward
            print(f"reward = {reward}")
        score = new_score

    print(f"Game over! Final score = {score}, total reward = {total_reward}")