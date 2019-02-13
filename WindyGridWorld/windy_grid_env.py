from rl_glue import BaseEnvironment
import numpy as np

class windyEnvironment(BaseEnvironment):
    """
    Defines the interface of an RLGlue environment

    ie. These methods must be defined in your own environment classes
    """


    def __init__(self):
        
        """Declare environment variables."""
        self.X = None
        self.Y = None
        self.currentState = None
        self.prevState = None
        self.i = None
        
        
        

    def env_init(self):
        """
        Initialize environment variables.
        """
        

    def env_start(self):
        """
        The first method called when the experiment starts, called before the
        agent starts.

        Returns:
            The first state observation from the environment.
        """
        #first state is always 0,3
        return (0,3)

    def env_step(self, action):
        """
        A step taken by the environment.

        Args:
            action: The action taken by the agent

        Returns:
            (float, state, Boolean): a tuple of the reward, state observation,
                and boolean indicating if it's terminal.
        """
        #terminal state
        if(action == (7,3)):
            return 0, action, True
        
        state = [action[0], action[1]]
        
        #windy area. Get pushed up by 1
        if (action[0] >= 3 and action[0] <=5 or action[0] == 8):
            state[1] = action[1]-1
        #windy area. Get pushed up by 2
        elif (action[0] >=6 and action[0] <= 7):
            state[1] = action[1]-2
        
        #x can't go out of bounds
        if(state[0] < 0):
            x = 0
            
        elif (state[0] > 9):
            x = 9
            
        #x is the current state if it didn't go out of bounds
        else:
            x = state[0]
           
        #checks if y is out of bounds 
        if(state[1] < 0):
            y = 0
        elif (state[1] > 7):
            y = 7
        #y is set to the current state if it isn't
        else:
            y = state[1]
        
        return -1,(x,y),False
        
        

    def env_message(self, message):
        """
        receive a message from RLGlue
        Args:
           message (str): the message passed
        Returns:
           str: the environment's response to the message (optional)
        """
