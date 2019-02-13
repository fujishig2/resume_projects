from rl_glue import BaseAgent
import numpy as np

class Agent_epsilon01(BaseAgent):
    def __init__(self):
        """Declare agent variables."""

        #previous action made
        self.prevAction = None

        #list of estimates from all the previous actions
        self.estimates = None

    def agent_init(self):
        """Initialize agent variables."""
        self.estimates = []
        for i in range(10):
            #initially estimates (Q(a)) are all set to 0
            self.estimates.append(0)

    def _choose_action(self, state):
        """
        Convenience function.
        """
        #This agent will either choose the greedy action with the best estimate
        #or 1/10 times it will indiscriminately choose a random action.
        if (np.random.randint(10) >= 1):
            maxi = 0
            i = 0
            for estimate in self.estimates:
                if estimate > maxi:
                    maxi = estimate
                    state = i
                i += 1
            return state
        else:
            state = np.random.randint(10)
            return state          
                

    def agent_start(self, state):
        """
        The first method called when the experiment starts, called after
        the environment starts.
        Args:
            state (state observation): The agent's current state

        Returns:
            The first action the agent takes.
        """
        
        self.prevAction = self._choose_action(state)
        return self.prevAction

    def agent_step(self, reward, state):
        """
        A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (state observation): The agent's current state
        Returns:
            The action the agent is taking.
        """
        
        #estimates are updated here. The formula is as follows:
        #Q(a) = Q(a) + alpha*(R(a) - Q(a)), where alpha = 0.1     
        self.estimates[state] += 0.1*(reward - self.estimates[state])
        self.prevAction = self._choose_action(state)

        return self.prevAction

    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """
        pass

    def agent_message(self, message):
        pass