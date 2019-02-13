from rl_glue import BaseAgent
import numpy as np
from tile3 import tiles, IHT

class Agent(BaseAgent):
    """
    Defines the interface of an RLGlue Agent

    ie. These methods must be defined in your own Agent classes
    """
    
    
    def __init__(self):
        """Declare agent variables."""
        self.weights = None
        self.features = None
        self.Q = None
        self.old_Q = None
        self.alpha = None  
        self.iht = None
        self.lam = None
        self.delta = None
        self.z = None
        self.z_features = None

    
    def agent_init(self):
        """Initialize agent variables."""
        self.iht = IHT(4096)
        self.weights = dict()
        self.features = dict()
        self.z = dict()
        for i in range(4096):
            self.weights[i] = np.random.uniform(-0.001,0)
        self.z_features = []
        self.alpha = 0.1/8    
        self.lam = 0.9
        self.delta = 0
        self.Q = 0
        self.old_Q = 0     

    
    def agent_start(self, state):
        """
        The first method called when the experiment starts, called after
        the environment starts.
        Args:
            state (state observation): The agent's current state

        Returns:
            The first action the agent takes.
        """
        estimates = []
        self.Q = 0
        best_A = 0
        features = dict()
        
        for i in range(3):
            features[i] = tiles(self.iht, 8, [8*state[0]/(1.7), 8*state[1]/(0.14)], [i])
            estimates.append(0)
            for feature in features[i]:
                estimates[i] += self.weights[feature]
        
            if estimates[i] >= estimates[best_A]:
                self.Q = estimates[i]
                self.features[1] = features[i]
                best_A = i
        
        for i in range(4096):
            self.z[i] = 0
        self.z_features = []
        
        return best_A

    
    def agent_step(self, reward, state):
        """
        A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (state observation): The agent's current state
        Returns:
            The action the agent is taking.
        """
        self.old_Q = self.Q
        estimates = []
        self.Q = 0
        best_A = 0
        self.features[0] = self.features[1]
        features = dict()
        
        for i in range(3):
            features[i] = tiles(self.iht, 8, [8*state[0]/(1.7), 8*state[1]/(0.14)], [i])
            estimates.append(0)
            for feature in features[i]:
                estimates[i] += self.weights[feature]
        
            if estimates[i] >= estimates[best_A]:
                self.Q = estimates[i]
                self.features[1] = features[i]
                best_A = i     
                
        self.delta = reward + self.Q - self.old_Q
        
        for feature in self.features[0]:
            self.delta -= self.weights[feature]
            self.z[feature] += 1
            if feature not in self.z_features:
                self.z_features.append(feature)
        
        for feature in self.features[1]:
            self.delta += self.weights[feature]
            
        for feature in self.z_features:
            self.weights[feature] += self.alpha*self.delta*self.z[feature]
            self.z[feature] *= self.lam
        
        
        return best_A

    
    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """
        self.delta = reward - self.Q
        for feature in self.z_features:
            self.weights[feature] += self.alpha*self.delta*self.z[feature]

    def agent_message(self, message):
        """
        receive a message from rlglue
        args:
            message (str): the message passed
        returns:
            str : the agent's response to the message (optional)
        """
        steps = 50
        all_values = []
        for i in range(steps):
            all_values.append([])
            for j in range(steps):
                values = []
                for a in range(3):
                    inds = tiles(self.iht, 8, [8*(-1.2+(i*1.7/steps)), 8*(-0.07 + (j*0.14/steps))], [a])
                    sums = 0
                    for ind in inds:
                        sums += self.weights[ind]
                    values.append(sums)
                height = max(values)
                all_values[i].append(-height)
                
            
        return all_values