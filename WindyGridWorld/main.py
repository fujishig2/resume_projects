from sarsa8_agent import sarsa8Agent
from sarsa9_agent import sarsa9Agent
from windy_grid_env import windyEnvironment
from rl_glue import RLGlue
import matplotlib.pyplot as plt
import numpy as np


def main():
    #declare variables
    sarsa8 = sarsa8Agent()
    env8 = windyEnvironment()
    rlglue8 = RLGlue(env8, sarsa8)
    sarsa9 = sarsa9Agent()
    env9 = windyEnvironment()
    rlglue9 = RLGlue(env9, sarsa9)    
    del sarsa8, env8, sarsa9, env9
    
    #setup variables and initialize rlglue
    Yvalue8 = []
    rlglue8.rl_init()
    Yvalue9 = []
    rlglue9.rl_init()    
    terminal8 = True
    episodes8 = 0
    terminal9 = True
    episodes9 = 0
    
    #for 8000 steps run this problem
    for i in range(8000):
        #sarsa 8 step is here:
        if (terminal8):
            #restart the episode when an episode ends
            episodes8 += 1
            rlglue8.rl_start()
            terminal8 = False
        else:
            #do a step in 8-step sarsa windy gridworld.
            reward, state, last_action, terminal8 = rlglue8.rl_step()
            
        #sarsa 9-step is here:
        if (terminal9):
            episodes9 += 1
            rlglue9.rl_start()
            terminal9 = False
        else:
            reward, state, last_action, terminal9 = rlglue9.rl_step()
            
        #counts the number of episodes per time step
        Yvalue8.append(episodes8)
        Yvalue9.append(episodes9)
        
    #plot figure 1
    Xvalues = np.arange(0, 8000)
    plt.figure(1)
    plt.plot(Xvalues, Yvalue8, label = "8 step windy gridworld, epsilon = 0.1, alpha = 0.5")
    plt.grid(True)
    plt.legend()
    plt.xlabel('Time steps')
    plt.ylabel('Episodes')
   
    #plot figure 2
    plt.figure(2)
    plt.plot(Xvalues, Yvalue9, label = "9 step windy gridworld, epsilon = 0.1, alpha = 0.5")
    plt.grid(True)
    plt.legend()
    plt.xlabel('Time steps')
    plt.ylabel('Episodes')    
    plt.show()          

if __name__ == '__main__':
    main()