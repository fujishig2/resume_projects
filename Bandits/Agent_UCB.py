from rl_glue import BaseAgent
import numpy as np
import math

class Agent_UCB(BaseAgent):
    def __init__(self):
        """Declare agent variables."""
        
        #previous action made
        self.prevAction = None
        
        #A list containing counts of how many times each available action was made
        self.Actions = None

        #list of estimates from all the previous actions
        self.estimates = None
        
        #Counts all steps made
        self.time = None

    def agent_init(self):
        """Initialize agent variables."""
        self.estimates = []
        self.Actions = []
        self.time = 0
        for i in range(10):
            #initially estimates (Q(a)) are all set to 0
            self.estimates.append(0)
            self.Actions.append(0)

    def _choose_action(self, state):
        """
        Convenience function.
        """
        
        maxi = 0
        i = 0
        #looks at all the estimates. It will either choose an estimate that hasn't
        #been looked at yet, or chooses the best estimate with the best max UCB.
        for estimate in self.estimates:
            if self.Actions[i] != 0:
                At = estimate + 2*math.sqrt(math.log(self.time)/self.Actions[i])
                if At > maxi:
                    maxi = At
                    state = i
            else:
                state = i
                break
            i += 1
        self.Actions[state] += 1
        self.time += 1
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
        #Q(a) = Q(a) + 1/N(a)*(R(a) - Q(a))
        self.estimates[state] += 1/self.Actions[state]*(reward - self.estimates[state])
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