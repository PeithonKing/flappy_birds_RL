from flappy_bird_ai import *
import random

    
def get_state(game):
    """returns an array of the form:
    [
            # used now 
        1. x-distance of bird from front wall of obstacle,
        2. x-distance of bird from back wall of obstacle,
        3. y-distance of bird from upper wall of obstacle,
        4. y-distance of bird from lower wall of obstacle,
        5. v of bird
            # future improvements
        6. v of obstacle
        7. s of bird
        8. jump_height of bird
        9. accelaration due to gravity
    ]
    
    so for now, we have 9 features, and it returns an array of length 5.
    """
    pipe = game.obstacle
    bird = game.birds[0]
    return [
        # 1. x-distance of bird from front wall of obstacle
        pipe.x - bird.x,
        
        # 2. x-distance of bird from back wall of obstacle
        pipe.x - bird.x + pipe.length,
        
        # 3. y-distance of bird from upper wall of obstacle
        pipe.gap_y - 0.5*pipe.gap - bird.s,
        
        # 4. y-distance of bird from lower wall of obstacle
        pipe.gap_y + 0.5*pipe.gap - bird.s,
        
        # 5. v of bird
        bird.v
    ]

def get_action(state):
    dx1, dx2, dy1, dy2, v = state
    threshold = v*0.2 + 10
    if threshold > dy2:
        return [1, 0]
    return [0, 1]

def play():
    total_reward = 0
    game = FlappyBird()
    while True:
        # get current state
        state_old = get_state(game)
        
        # print(f"state_old: {state_old}")
        
        # ask the model to predict the action
        predicted_move = get_action(state_old)
        
        # do action
        reward, game_over, score = game.play_step([predicted_move])
        total_reward += reward
        if game_over:
            return score


if __name__ == "__main__":
    print(f"score = {play()}")
    