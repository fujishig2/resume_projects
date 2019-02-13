"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018,
  University of Alberta.
  Gambler's problem environment using RLGlue.
"""
from rl_glue import BaseEnvironment
import numpy as np


class GamblerEnvironment(BaseEnvironment):
    """
    Slightly modified Gambler environment -- Example 4.3 from
    RL book (2nd edition)

    Note: inherit from BaseEnvironment to be sure that your Agent class implements
    the entire BaseEnvironment interface
    """

    def __init__(self):
        """Declare environment variables."""

        # state we are in currently
        self.currentState = None
        
        #probability of winning
        self.probs = 0
    def env_init(self):
        """
        Arguments: Nothing
        Returns: Nothing
        Hint: Initialize environment variables necessary for run.
        """
        #initialize probability of winning to 0.55
        self.probs = 25

    def env_start(self):
        """
        Arguments: Nothing
        Returns: state - numpy array
        Hint: Sample the starting state necessary for exploring starts and return.
        """
        #choose a random start state
        self.currentState = np.random.randint(1, high = 101)
        return self.currentState        

    def env_step(self, action):
        """
        Arguments: action - integer
        Returns: reward - float, state - numpy array - terminal - boolean
        Hint: Take a step in the environment based on dynamics; also checking for action validity in
        state may help handle any rogue agents.
        """
        #make a random number from 1 to 100
        temp = np.random.randint(1,high = 101)
        #check to see if the random number is within the range of Ph.
        #if it isn't, we lose the amount made in action
        if (temp > self.probs):
            action = -action
        
        terminal = False
        reward = 0
        self.currentState += action
        
        #check to see if the current state is a termination state
        if (self.currentState >= 100):
            terminal = True
            reward = 1
        if (self.currentState <= 0):
            terminal = True
        
        
        return reward, self.currentState, terminal
        

    def env_message(self, in_message):
        """
        Arguments: in_message - string
        Returns: response based on in_message
        This function is complete. You do not need to add code here.
        """
        pass
