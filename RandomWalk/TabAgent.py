from rl_glue import BaseAgent
import numpy as np

class TabularAgent(BaseAgent):
    """
    Defines the interface of an RLGlue Agent

    ie. These methods must be defined in your own Agent classes
    """

    def __init__(self):
        """Declare agent variables."""
        self.weights = None
        self.prevState = None
        self.state = None
        self.alpha = None

    def agent_init(self):
        """Initialize agent variables."""
        self.weights = dict()
        for i in range(1000):
            self.weights[i] = 0
        self.prevState = 0
        self.state = 0       
        self.alpha = 0.5

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
        self.prevState = self.state
        self.state = state-1
        
        #update using regular TD(0)
        self.weights[self.prevState] = self.weights[self.prevState] + self.alpha*(reward+self.weights[self.state]-self.weights[self.prevState])
        return self.prevState
        

    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """
        self.prevState = self.state   
                
        #update using regular TD(0)
        self.weights[self.prevState] = self.weights[self.prevState] + self.alpha*(reward-self.weights[self.prevState])      

    def agent_message(self, message):
        """
        receive a message from rlglue
        args:
            message (str): the message passed
        returns:
            str : the agent's response to the message (optional)
        """
        #weight is the value function because each feature corresponds
        #to the each state
        return self.weights