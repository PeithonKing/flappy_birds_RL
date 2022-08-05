import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

# game loop
running = True
while running:
    screen.fill("#000000") # black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("yes")
        

    
    pygame.display.update()
