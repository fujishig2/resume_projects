from rl_glue import BaseEnvironment
import numpy as np

class walkEnv(BaseEnvironment):
    """
    Defines the interface of an RLGlue environment

    ie. These methods must be defined in your own environment classes
    """
    def __init__(self):
        """Declare environment variables."""
        self.currentState = None

    def env_init(self):
        """
        Initialize environment variables.
        """
        self.currentState = 500

    def env_start(self):
        """
        The first method called when the experiment starts, called before the
        agent starts.

        Returns:
            The first state observation from the environment.
        """
        self.currentState = 500
        return self.currentState       

    def env_step(self, action):
        """
        A step taken by the environment.

        Args:
            action: The action taken by the agent

        Returns:
            (float, state, Boolean): a tuple of the reward, state observation,
                and boolean indicating if it's terminal.
        """
        self.currentState += np.random.randint(-100, high=101)
        terminal = False
        reward = 0
        if (self.currentState > 1000):
            reward = 1
            terminal = True
        elif (self.currentState < 1):
            terminal = True
            reward = -1
        return reward, self.currentState, terminal
        
    def env_message(self, message):
        """
        receive a message from RLGlue
        Args:
           message (str): the message passed
        Returns:
           str: the environment's response to the message (optional)
        """
