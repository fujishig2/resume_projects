"""
   Purpose: For use in the Reinforcement Learning course, Fall 2018,
   University of Alberta.
   Monte Carlo agent using RLGlue - barebones.
"""
from rl_glue import BaseAgent
import numpy as np


class MonteCarloAgent(BaseAgent):
    """
    Monte Carlo agent -- Section 5.3 from RL book (2nd edition)

    Note: inherit from BaseAgent to be sure that your Agent class implements
    the entire BaseAgent interface
    """

    def __init__(self):
        """Declare agent variables."""
        self.policy = None
        self.Q = None
        self.returns = None
        self.G = None
        self.states = None
        self.step = None
        self.rewards = None
        self.actions = None

    def agent_init(self):
        """
        Arguments: Nothing
        Returns: Nothing
        Hint: Initialize the variables that need to be reset before each run
        begins
        """
        self.policy = []
        self.Q = []
        self.returns = []
        self.G = 0
        self.step = 0
        self.rewards = []
        self.actions = []
        self.states = []
        
        for i in range(101):
            #setup policies
            #self.policy.append(min(i, 100-i))
            bet = i % 2
            if (bet == 0 and i > 0 and i < 100):
                bet = 2
            self.policy.append(bet)
            self.Q.append([])
            self.returns.append([])
            for j in range(51):
                #setup Q(s,a) = 0.069 for all available values to promote exploration
                self.Q[i].append(0)
                if (j <= min(i, 100-i) and j > 0):
                    self.Q[i][j] = 0.069
                self.returns[i].append([])        
                

    def agent_start(self, state):
        """
        Arguments: state - numpy array
        Returns: action - integer
        Hint: Initialize the variables that you want to reset before starting
        a new episode, pick the first action, don't forget about exploring
        starts
        """
        #these variables must be blank every episode
        self.G = 0
        self.rewards = []
        self.states = []
        self.actions = []
        self.step = 0
        
        #save the start state and first action taken
        self.states.append(state)
        self.step += 1
        action = self.policy[state]
        self.actions.append(action)
        return action
        
        
        
        

    def agent_step(self, reward, state):
        """
        Arguments: reward - floting point, state - numpy array
        Returns: action - integer
        Hint: select an action based on pi
        """
        #save the current state, and action taken
        self.states.append(state)
        self.step += 1
        self.rewards.append(reward)
        action = self.policy[state]
        self.actions.append(action)
        return action
        

    def agent_end(self, reward):
        """
        Arguments: reward - floating point
        Returns: Nothing
        Hint: do necessary steps for policy evaluation and improvement
        """
        
        self.rewards.append(reward)
        
        #go backwards from the terminal state
        for i in range(self.step-1, -1, -1):
            
            #evaluate Gt to be Gt + Rt+1
            self.G = self.G + self.rewards[i]
            
            #if the state and action at time t wasn't taken before during this episode
            if ((self.states[i] not in self.states[0:i]) and (self.actions[i] not in self.actions[0:i])):
                
                #returns appends g at St = s and At = a
                self.returns[self.states[i]][self.actions[i]].append(self.G)
            
                avg = 0
                count = 0
                #take the average of all the returns at St = s and At = a
                for ret in self.returns[self.states[i]][self.actions[i]]:
                    avg += ret
                    count += 1
                avg = avg/count
                
                #Q at St = s and At = a is now the average of all the returns
                self.Q[self.states[i]][self.actions[i]] = avg
                
                #find the largest Q at St = s and At = a. 
                #The action with the highest estimate is the policy
                largest_Q = self.Q[self.states[i]][1]
                index = 1
                for j in range(1, 51):
                    if (self.Q[self.states[i]][j] > largest_Q):
                        largest_Q = self.Q[self.states[i]][j]
                        index = j
                self.policy[self.states[i]] = index
                

    def agent_message(self, in_message):
        """
        Arguments: in_message - string
        Returns: The value function as a list.
        This function is complete. You do not need to add code here.
        """
        if in_message == 'ValueFunction':
            return (np.max(self.Q, axis=1)).tostring()
        else:
            return "I dont know how to respond to this message!!"


        
        
