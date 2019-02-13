from Agent_epsilon00 import Agent_epsilon00
from Agent_epsilon01 import Agent_epsilon01
from Agent_UCB import Agent_UCB
from bandit_env import bandit_env
from rl_glue import RLGlue
import matplotlib.pyplot as plt
import numpy as np


def main():
    #Declaring all the averages as a list
    Yaverages00 = []
    Yaverages01 = []
    YaveragesUCB = []
    for l in range(1000):
        #create 1000 zeros in each of the averages
        Yaverages00.append(0)
        Yaverages01.append(0)
        YaveragesUCB.append(0)
         
    for l in range(2000):
        #create, initialize, and start the rlglue type objects
        agent00 = Agent_epsilon00()
        agent01 = Agent_epsilon01()
        agentUCB = Agent_UCB()
        env00 = bandit_env()
        env01 = bandit_env()
        envUCB = bandit_env()
        rlglue00 = RLGlue(env00, agent00)
        rlglue01 = RLGlue(env01, agent01)
        rlglueUCB = RLGlue(envUCB, agentUCB)
        #delete the variables not being used
        del agent00, agent01, agentUCB, env00, env01, envUCB
        
        rlglue00.rl_init()
        rlglue01.rl_init()
        rlglueUCB.rl_init()
        state00, x = rlglue00.rl_start()
        state01, x =rlglue01.rl_start()
        stateUCB, x =rlglueUCB.rl_start()
        
        #if the state is the optimal state, we incriment the averages variable at
        #that time step by 1
        optimal00 = rlglue00.rl_env_message(None)
        optimal01 = rlglue01.rl_env_message(None)
        optimalUCB = rlglueUCB.rl_env_message(None)
        if state00 == optimal00:
            Yaverages00[0] += 1
        if state01 == optimal01:
            Yaverages01[0] += 1
        if stateUCB == optimalUCB:
            YaveragesUCB[0] += 1
        
        
        for i in range(1, 1000):
            t, x, state00, s = rlglue00.rl_step()
            t, x, state01, s =rlglue01.rl_step()
            t, x, stateUCB, s =rlglueUCB.rl_step()
            #if the state is the optimal state, we incriment the averages variable at
            #that time step by 1
            if state00 == optimal00:
                Yaverages00[i] += 1
            if state01 == optimal01:
                Yaverages01[i] += 1
            if stateUCB == optimalUCB:
                YaveragesUCB[i] += 1
        
    #adjusts all the averages
    for i in range(1000):
        Yaverages00[i] = Yaverages00[i]/20
    for i in range(1000):
        Yaverages01[i] = Yaverages01[i]/20
    for i in range(1000):
        YaveragesUCB[i] = YaveragesUCB[i]/20 
            
                
    #plot the graphs made from taking the average % optimal step over 2000 runs
    Xvalues = np.arange(0, 1000)
    plt.plot(Xvalues, Yaverages00, label = "epsilon 0, Q(a) = 5, alpha = 0.1")
    plt.plot(Xvalues, Yaverages01, label = "epsilon 0.1, Q(a) = 0, alpha = 0.1")
    plt.plot(Xvalues, YaveragesUCB, label = "UCB, Q(a) = 0, alpha = 1/N(a), c = 2")
    plt.grid(True)
    plt.legend()
    plt.xlabel('Steps')
    plt.ylabel('% Optimal Action')
    plt.show()      
    
    
if __name__ == '__main__':
    main()