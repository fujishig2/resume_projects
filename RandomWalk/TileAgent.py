from rl_glue import BaseAgent
import numpy as np
from tiles3 import tiles, IHT

class TileAgent(BaseAgent):
    """
    Defines the interface of an RLGlue Agent

    ie. These methods must be defined in your own Agent classes
    """

    def __init__(self):
        """Declare agent variables."""
        self.weights = None
        self.features = None
        self.prevState = None
        self.state = None
        self.v = None
        self.old_v = None
        self.alpha = None  
        self.iht = None

    def agent_init(self):
        """Initialize agent variables."""
        self.iht = IHT(300)
        self.weights = dict()
        self.features = dict()
        scaleFactor = (5/1000)
        for i in range(1000):
            self.features[i] = tiles(self.iht, 50, [i*scaleFactor])
        for i in range(300):
            self.weights[i] = 0
        
        self.prevState = 0
        self.state = 0       
        self.v = 0
        self.old_v = 0
        self.alpha = 0.01/50    

    def agent_start(self, state):
        """
        The first method called when the experiment starts, called after
        the environment starts.
        Args:
            state (state observation): The agent's current state

        Returns:
            The first action the agent takes.
        """
        self.state = state-1
        self.v = 0
        #update v as the sum of all weights for current state*features
        for feature in self.features[self.state]:
            self.v += self.weights[feature]
        return self.state
        
        
 

    def agent_step(self, reward, state):
        """
        A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (state observation): The agent's current state
        Returns:
            The action the agent is taking.
        """
        self.old_v = self.v
        self.v = 0
        self.prevState = self.state
        self.state = state-1
        #update v as the sum of all weights for current state*features
        for feature in self.features[self.state]:
            self.v += self.weights[feature]
        
        #update the previous states weights according to TD(0) update.
        for feature in self.features[self.prevState]:
            self.weights[feature] += self.alpha*(reward + self.v - self.old_v)
        return self.state

    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """
        self.old_v = self.v
        self.prevState = self.state        
        #update the previous states weights according to TD(0) update.
        for feature in self.features[self.prevState]:
            self.weights[feature] += self.alpha*(reward - self.old_v)   

    def agent_message(self, message):
        """
        receive a message from rlglue
        args:
            message (str): the message passed
        returns:
            str : the agent's response to the message (optional)
        """
        #create the value function based off of its weights and features
        v = dict()
        for i in range(1000):
            v[i] = 0
            for feature in self.features[i]:
                v[i] += self.weights[feature]
        
        return v