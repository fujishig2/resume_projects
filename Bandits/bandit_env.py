from rl_glue import BaseEnvironment
import numpy as np

class bandit_env(BaseEnvironment):
    
    def __init__(self):
        """Declare environment variables."""

        # state we always start in
        self.startState = None

        # state we are in currently
        self.currentState = None
        
        #optimal choice
        self.optimal = None
        
        #List of reward means
        self.probs = None

    def env_init(self):
        """
        Initialize environment variables.
        """
        self.startState = 0
        self.probs = []
        self.optimal = 0
        best = -10
        for i in range(10):
            #Creates 10 random means, distributed under a normal curve with 0 as the mean, and variance = 1.
            self.probs.append(np.random.normal(0, 1))
            if best < self.probs[i]:
                best = self.probs[i]
                self.optimal = i
        
        

    def env_start(self):
        """
        The first method called when the experiment starts, called before the
        agent starts.

        Returns:
            The first state observation from the environment.
        """
        self.currentState = self.startState
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
        terminal = False

        # This environment will give a randomly selected variable across a
        # normal distribution with variance 1 and the value in probs as the mean.
        reward = np.random.normal(self.probs[action], 1)
        
        return reward, action, terminal

    def env_message(self, message):
        return self.optimal