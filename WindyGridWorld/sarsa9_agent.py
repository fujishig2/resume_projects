from rl_glue import BaseAgent
import numpy as np

class sarsa9Agent(BaseAgent):
    """
    Defines the interface of an RLGlue Agent

    ie. These methods must be defined in your own Agent classes
    """

    def __init__(self):
        """Declare agent variables."""
        self.Q = None
        self.policy = None
        self.epsilon = None
        self.actions = None
        self.prevState = None
        self.alpha = None
        self.i = None

    def agent_init(self):
        """Initialize agent variables."""
        
        self.policy = 0
        self.epsilon = 0.1
        self.alpha = 0.5
        self.Q = dict()
        for x in range(0, 10):
            for y in range(0,8):
                for A in range(9):
                    self.Q[((x,y),A)] = 0
        
        self.actions = {
            0: (-1,-1),
            1: (0, -1),
            2: (1, -1),
            3: (1, 0),
            4: (1, 1),
            5: (0, 1),
            6: (-1, 1),
            7: (-1, 0),
            8: (0,0)
        }   
        

    def agent_start(self, state):
        """
        The first method called when the experiment starts, called after
        the environment starts.
        Args:
            state (state observation): The agent's current state

        Returns:
            The first action the agent takes.
        """
        self.i = 0
        greedy = np.random.uniform()
        self.prevState = state
        #take the greedy action if we are above epsilon
        if (greedy > self.epsilon):
            best_V = 0
            ties = [0]
            for A in range(9):
                #find the best value out of the 9 possible actions
                if (best_V < self.Q[(state, A)]):
                    best_V = self.Q[(state, A)]
                    ties = [A]
                elif (best_V == self.Q[(state, A)]):
                    ties.append(A)
                
            #policy is a random choice from all the states with highest values
            self.policy = ties[np.random.randint(0, high=len(ties))]
            
            return (state[0]+self.actions[self.policy][0], state[1]+self.actions[self.policy][1])
        
        #epsilon action
        else:
            self.policy = np.random.randint(0, high=8)
            return (state[0]+self.actions[self.policy][0], state[1]+self.actions[self.policy][1])
        

    def agent_step(self, reward, state):
        """
        A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (state observation): The agent's current state
        Returns:
            The action the agent is taking.
        """
        greedy = np.random.uniform()
       
        last_action = self.policy        
        #take the greedy action
        if (greedy > self.epsilon):
            #find the best current states value
            best_V = -2000000
            ties = []
            for A in range(9):
                if (best_V < self.Q[(state, A)]):
                    best_V = self.Q[(state, A)]
                    ties = [A]
                elif (best_V == self.Q[(state, A)]):
                    ties.append(A)
            self.policy = ties[np.random.randint(0, high=len(ties))]
                        
    
        #take the epsilon action
        else:
            self.policy = np.random.randint(0, high=8)
                
        #update Q(s,a) to be Q(s,a)+alpha*(R + maxQ(s',a)-Q(s,a))
        self.Q[(self.prevState, last_action)] = self.Q[(self.prevState, last_action)] + self.alpha*(reward + self.Q[(state, self.policy)] - self.Q[(self.prevState, last_action)])
        self.prevState = state          
        return (state[0]+self.actions[self.policy][0], state[1]+self.actions[self.policy][1])
        

    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """

    def agent_message(self, message):
        """
        receive a message from rlglue
        args:
            message (str): the message passed
        returns:
            str : the agent's response to the message (optional)
        """
        
