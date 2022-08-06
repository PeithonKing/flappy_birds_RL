import torch
import random
# import numpy as np
from flappy_bird_ai import *
from collections import deque
from model import QTrainer, Linear_QNet
from plotting import plot
import matplotlib.pyplot as plt 

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

# 

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # exploration rate
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(5, 5, 2)
        self.trainer = QTrainer(self.model, LR, self.gamma)
    
    def get_state(self, game):
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

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_reward = 0
    total_score = 0
    record = 0
    agent = Agent()
    game = FlappyBird()
    while True:
        # get current state
        state_old = agent.get_state(game)
        
        # print(f"state_old: {state_old}")
        
        # ask the model to predict the action
        predicted_move = agent.get_action(state_old)
        
        # do action
        reward, game_over, score = game.play_step([predicted_move])
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, predicted_move, reward, state_new, game_over)
        agent.remember(state_old, predicted_move, reward, state_new, game_over)
        
        total_reward += reward
        
        if game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                # save the model
                agent.model.save()
            
            print(f"Game: {agent.n_games} Score: {score} Record: {record} Total Reward: {total_reward}")
            total_reward = 0
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()