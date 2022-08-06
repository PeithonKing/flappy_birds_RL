from flappy_bird_ai import *
import random
import pandas as pd
import string

    
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
        10. last jump time
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
        bird.v,
        
        # 10. last jumped
        game.last_jumped
    ]

def get_action(state): # ai version
    dx1, dx2, dy1, dy2, v, last_jumped = state
    if not v: v=1
    threshold = v*0.2 + 10
    cool_down = (time.time()-last_jumped)*v/10
    if threshold > dy2 and cool_down > 1:
        # print(f"cool down = {cool_down}")
        return [[1, 0], threshold] # jump
    return [[0, 1], threshold]

def play():
    total_reward = 0
    game = FlappyBird()
    t0 = time.time()-0.01
    data = {
        "x1": [],
        "x2": [],
        "x3": [],
        "x4": [],
        "x5": [],
        "x6": [],
        "y": [],  # predicted_move[0] (jump or not)
    }
    while True:
        # get current state
        state_old = get_state(game)
        
        x1, x2, x3, x4, x5, x6 = state_old
        
        # print(f"state_old: {state_old}")
        
        # ask the model to predict the action
        predicted_move, threshold = get_action(state_old)
        
        
        # do action
        reward, game_over, score, t0 = game.play_step(
                    actions = [predicted_move], 
                    threshold = int(threshold), 
                    t0 = t0
            )
        total_reward += reward
        
        # add to data
        data["x1"].append(x1)
        data["x2"].append(x2)
        data["x3"].append(x3)
        data["x4"].append(x4)
        data["x5"].append(x5)
        data["x6"].append((time.time()-x6)*1000)
        data["y"].append(predicted_move[0])
        
        if game_over:
            return score, data  # pd.DataFrame(data).T

if __name__ == "__main__":
    
    data = {
        "x1": [],
        "x2": [],
        "x3": [],
        "x4": [],
        "x5": [],
        "x6": [],
        "y": [],  # predicted_move[0] (jump or not)
        }

    for i in range(5):
        score, new_data = play()
        print(f"score = {score}")
        for key, value in new_data.items():
            data[key] += value

    name = "".join(random.choice(string.ascii_letters+"0123456789"*5) for _ in range(20))
    
    if len(data["y"]) > 500: pd.DataFrame(data).to_csv(f"data_for_supervised_learning/{name}.csv", index=False)
    
