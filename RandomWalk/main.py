from TabAgent import TabularAgent
from TileAgent import TileAgent
from rWalkEnv import walkEnv
from rl_glue import RLGlue
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime

def main():
    start = datetime.now()
    
    #declare variables
    TabA = TabularAgent()
    TileA = TileAgent()
    EnvTab = walkEnv()
    EnvTile = walkEnv()
    rlTab = RLGlue(EnvTab, TabA)
    rlTile = RLGlue(EnvTile, TileA)
    del TabA, EnvTab, TileA, EnvTile
    true_v = np.load('true_v.npy').item()   #obtained from running DP.py
    tabRMS = []
    tileRMS = []
    
    for k in range(200):
        tabRMS.append(0)
        tileRMS.append(0)
    
    #setup 30 runs
    for k in range(30):
        rlTab.rl_init()
        rlTile.rl_init()
        count = 0
        #setup 2000 episodes
        for i in range(2000):
            rlTab.rl_start()
            rlTile.rl_start()
            terminal = False
            while not terminal:
                _,_,_, terminal = rlTile.rl_step()
                _,_,_, terminal = rlTab.rl_step()
                
            #check value RMSE
            if(i % 10 == 0):
                tile_v = rlTile.rl_agent_message(None)
                tab_v = rlTab.rl_agent_message(None)
                tile_sq_err = 0
                tab_sq_err = 0
                for j in range(1000):
                    tile_sq_err += (true_v[j]-tile_v[j])**2
                    tab_sq_err += (true_v[j]-tab_v[j])**2
                tile_sq_err /= 1000
                tab_sq_err /= 1000
                
                #update the running average of stored RMSE values
                tileRMS[count] = (k*tileRMS[count] + math.sqrt(tile_sq_err))/(k+1)
                tabRMS[count] = (k*tabRMS[count] + math.sqrt(tab_sq_err))/(k+1)
                count += 1
                
    #plot the 2000 episodes averaged over 30 runs
    Xvalues = np.arange(0,2000, 10)
    plt.plot(Xvalues, tabRMS, label = "TD(0) one-hot RMSE")
    plt.plot(Xvalues, tileRMS, label = "TD(0) tile coding RMSE")
    plt.grid(True)
    plt.legend()
    plt.xlabel('Episodes')
    plt.ylabel('RMSE') 
    plt.show()
    
    print("Time until completion:", datetime.now()-start)
    
if __name__ == '__main__':
    main()