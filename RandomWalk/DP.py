import numpy as np

class DP():
    
    def __init__(self):
        self.theta = None
        self.V = None
        self.delta = None
        
    #get the true value function using DP
    def getValue(self):
        self.V = dict()
        for i in range(1000):
            self.V[i] = 0        
        self.delta = 1
        
        #theta is a number very close to zero to ensure lots of accuracy
        self.theta = 0.00000000000000000000000000000000000000000000000000000000000000001
        
        while self.delta >= self.theta:
            self.delta = 0
            for i in range(1000):
                low = 100
                high = 101
                v = self.V[i]
                sums = 0
                
                for k in range(i-low, i+high):
                    if k < 0:
                        sums += 1/200*(-1)
                    
                    elif k > 999:
                        sums += 1/200
                    else:
                        sums += (1/200)*self.V[k]
                        
                self.V[i] = sums
                self.delta = max(self.delta, abs(v-self.V[i]))
                
        return self.V

#used to store the dictionary of values into a .npy file
def main():
    x=DP
    v = x.getValue(x)
    np.save('true_v.npy', v)
    
if __name__ == '__main__':
    main()