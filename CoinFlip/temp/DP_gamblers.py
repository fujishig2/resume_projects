import matplotlib.pyplot as plt
import numpy as np
_, axs = plt.subplots(2, 2)

#helper function that finds the value function, as well as the optimal policy.
def value_create(state_values, rewards, policy, Ph):
    theta = 0.0001
    delta = theta
    #count = 0
    Xvalues = np.arange(0, 100)
    while (delta >= theta):
        delta = 0
        #count += 1
        #print(count)        
        #for each state
        for i in range(1,100):
            #print(i)
            
            #max bet is the state or 100-state
            if (i >= 50):
                max_bet = 100-i
            else:
                max_bet = i   
            #print(max_bet)
            #look for the action with the best estimate
            max_estimate = 0
            pol = 0
            for bet in range(1,max_bet+1):
                #in each action (bet), check to see if the estimate from this bet is the best
                if (Ph*(rewards[i+bet] + state_values[i+bet]) + (1-Ph)*(rewards[i-bet] + state_values[i-bet])) > max_estimate:
                    #update the temporary holders for best policy and best estimate
                    max_estimate = Ph*(rewards[i+bet] + state_values[i+bet]) + (1-Ph)*(rewards[i-bet] + state_values[i-bet])   
                    pol = bet
                    
            
            #get the difference from the old value and the new one
            old_v = state_values[i]        
            state_values[i] = max_estimate
            old_v = abs(old_v - state_values[i])
            #update the policy
            policy[i] = pol
            #update delta to be the max difference
            if(old_v > delta):
                delta = old_v   
        
        #setup the graph for each sweep
        if (Ph == 0.25):
            axs[0][0].plot(Xvalues, state_values[0:100])        
        else:
            axs[0][1].plot(Xvalues, state_values[0:100])
        
    
    return state_values, policy





def main():
    
    #initialize all the variables and fill them with zeros
    state_values = []
    policy_old = []
    policy_new = []
    rewards = []
    for i in range(100):
        state_values.append(0)
        policy_old.append(0)
        policy_new.append(0)
        rewards.append(0)
    policy_new.append(0)
    policy_old.append(0)
    state_values.append(0)
    #rewards at position 100 is 1
    rewards.append(1)
    
    
    #pH = 0.25 starts here:
    #gather the state values and policy values
    state_values, policy_new = value_create(state_values, rewards, policy_new, 0.25)
    #run this until the optimal policy found is found twice in a row
    non_equal = True
    
    while non_equal:
        non_equal = False
        #check to see if every state in the old policy is equal to the new one
        for i in range(101):
            if policy_old[i] != policy_new[i]:
                non_equal = True
                policy_old = policy_new
                    
                #regather the state values
                state_values, policy_new = value_create(state_values, rewards, policy_new, 0.25)
                
                
    #plot the pH = 0.25 graph on the first column
    axs[0][0].grid(True)
    axs[0][0].set_title('Ph = 0.25')
    axs[0][0].set_xlabel('Capital')
    axs[0][0].set_ylabel('Value estimates')
    
    Xvalues = np.arange(0, 101)
    axs[1][0].plot(Xvalues, policy_new)    
    axs[1][0].grid(True)
    axs[1][0].set_xlabel('Capital')
    axs[1][0].set_ylabel('Final policy (stake)')    
    
    #pH = 0.55 starts here:
    
    #reset all the values needed to obtain policy and state values
    #for pH = 0.55
    for i in range(101):
        state_values[i] = 0
        policy_old[i] = 0
        policy_new[i] = 0
        
        
    #gather the state values and policy values based off of new pH = 0.55
    state_values, policy_new = value_create(state_values, rewards, policy_new, 0.55)
    #run this until the optimal policy found is found twice in a row
    non_equal = True
    
    while non_equal:
        non_equal = False
        #check to see if every state in the old policy is equal to the new one
        for i in range(101):
            if policy_old[i] != policy_new[i]:
                non_equal = True
                policy_old = policy_new
                    
                #regather the state values
                state_values, policy_new = value_create(state_values, rewards, policy_new, 0.55)    
                
        
    #Plot the Ph = 0.55 graph on the second column
    axs[0][1].grid(True)
    axs[0][1].set_title('Ph = 0.55')
    axs[0][1].set_xlabel('Capital')
    axs[0][1].set_ylabel('Value estimates')
    axs[1][1].plot(Xvalues, policy_new)    
    axs[1][1].grid(True)
    axs[1][1].set_xlabel('Capital')
    axs[1][1].set_ylabel('Final policy (stake)')    
    plt.show()
        
if __name__ == '__main__':
    main()