"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018, University of Alberta.
  Implementation of the interaction between the Gambler's problem environment
  and the Monte Carlo agent using RLGlue.
"""
from rl_glue import RLGlue
from gambler_env import GamblerEnvironment
from mc_agent import MonteCarloAgent
import numpy as np

if __name__ == "__main__":
    num_episodes = 8000
    max_steps = 10000
    num_runs = 10

    # Create and pass agent and environment objects to RLGlue
    environment = GamblerEnvironment()
    agent = MonteCarloAgent()
    rlglue = RLGlue(environment, agent)
    del agent, environment  # don't use these anymore

    # episodes at which we are interested in the value function
    key_episodes = [99, 999, 7999]

    # dict to hold data for key episodes
    v_over_runs = {}
    for episode in key_episodes:
        v_over_runs[episode] = []

    for run in range(num_runs):
    #for run in range(1):

        print("run number: {}\n".format(run))

        # set seed for reproducibility
        np.random.seed(run)

        # initialize RL-Glue
        rlglue.rl_init()

        # loop over episodes
        for episode in range(num_episodes):

            # run episode with the allocated steps budget
            rlglue.rl_episode(max_steps)

            # if episode is one of the key episodes, extract and save value
            # function
            if episode in key_episodes:
                V = np.fromstring(rlglue.rl_agent_message('ValueFunction'),dtype='float')
                v_over_runs[episode].append(V)

    # extract length of key_episodes
    n_valueFunc = len(key_episodes)

    # extract number of states via length of a particular value function
    n = v_over_runs[key_episodes[0]][0].shape[0]

    # initialize data structure for average value function at key_episodes
    average_v_over_runs = np.zeros((n_valueFunc,n))

    # average across runs at various episodes, to estimate average value
    # function at episode
    for i, episode in enumerate(key_episodes):
        # each item in v_over_runs[episode] is a list (one item per run),
        # and each item is a value function

        # create a value function matrix of size (runs x number of states)
        data = np.matrix(v_over_runs[episode])

        # estimate average value function, across runs
        average_v_over_runs[i] = np.mean(data, axis=0)

    # save average value function numpy object, to be used by plotting script
    np.save("ValueFunction", average_v_over_runs)
