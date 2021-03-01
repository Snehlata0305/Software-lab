import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
if __name__ == '__main__':   
    data_file = sys.argv[2]
    df = pd.read_csv(data_file, sep=',')
    df = df.drop(["random_seed"], axis=1)
    groups = df.groupby(['instance', 'algorithm', 'epsilon', 'horizon']).mean()
    
    ep1_i1, ep2_i1, ep3_i1, kl1, rr1, ts1, ucb1 = groups[:7 :], groups[7:14 :], groups[14:21 :], groups[21:28 :], groups[28:35 :], groups[35:42 :], groups[42:49 :]
    ep1_i2, ep2_i2, ep3_i2, kl2, rr2, ts2, ucb2 = groups[49:56 :], groups[56:63 :], groups[63:70 :], groups[70:77 :], groups[77:84 :], groups[84:91 :], groups[91:98 :]
    ep1_i3, ep2_i3, ep3_i3, kl3, rr3, ts3, ucb3 = groups[98:105 :], groups[105:112 :], groups[112:119 :], groups[119:126 :], groups[126:133 :], groups[133:140 :], groups[140:147 :]
    
    for i in range(1,4):
        
        
        if i ==1:
            plt.xscale('log')
            plt.yscale('log')
            x=df['horizon'].unique()
            y1 = ep1_i1.values.flatten()
            plt.plot(x, y1, marker='o', label='Epsilon-greedy(0.002)')
            y2 = ep2_i1.values.flatten()
            plt.plot(x, y2, marker='o', label='Epsilon-greedy(0.02)')
            y3 = ep3_i1.values.flatten()
            plt.plot(x, y3, marker='o', label='Epsilon-greedy(0.2)')
            y4 = kl1.values.flatten()
            plt.plot(x, y4, marker='o', label='KL-UCB')
            y5 = rr1.values.flatten()
            plt.plot(x, y5, marker='o', label='Round-robin')
            y6 = ts1.values.flatten()
            plt.plot(x, y6, marker='o', label='Thomson-sampling')
            y7 = ucb1.values.flatten()
            plt.plot(x, y7, marker='o', label='UCB')
            plt.xlabel('Horizon')
            plt.ylabel('Regret')
            plt.title('instance-%d'%i)
            plt.legend()
            plt.savefig('instance%d.png'%i)
            plt.close()

        if i==2:
            plt.xscale('log')
            plt.yscale('log')
            x=df['horizon'].unique()
            y1 = ep1_i2.values.flatten()
            plt.plot(x, y1,marker='o', label='Epsilon-greedy(0.002)')
            y2 = ep2_i2.values.flatten()
            plt.plot(x, y2, marker='o', label='Epsilon-greedy(0.02)')
            y3 = ep3_i2.values.flatten()
            plt.plot(x, y3, marker='o', label='Epsilon-greedy(0.2)')
            y4 = kl2.values.flatten()
            plt.plot(x, y4, marker='o', label='KL-UCB')
            y5 = rr2.values.flatten()
            plt.plot(x, y5, marker='o', label='Round-robin')
            y6 = ts2.values.flatten()
            plt.plot(x, y6, marker='o', label='Thomson-sampling')
            y7 = ucb2.values.flatten()
            plt.plot(x, y7, marker='o', label='UCB')
            plt.xlabel('Horizon')
            plt.ylabel('Regret')
            plt.title('instance-%d'%i)
            plt.legend()
            plt.savefig('instance%d.png'%i)
            
            #plt.legend(()('Epsilon-greedy1', 'Epsilon-greedy2', 'Epsilon-greedy3', 'KL-UCB', 'Round-robin', 'Thomson-sampling', 'UCB')
            plt.close()
            
        if i==3:
            plt.xscale('log')
            plt.yscale('log')
            x=df['horizon'].unique()
            y1 = ep1_i3.values.flatten()
            plt.plot(x, y1, marker='o', label='Epsilon-greedy(0.002)')
            y2 = ep2_i3.values.flatten()
            plt.plot(x, y2, marker='o', label='Epsilon-greedy(0.02)')
            y3 = ep3_i3.values.flatten()
            plt.plot(x, y3, marker='o', label='Epsilon-greedy(0.2)')
            y4 = kl3.values.flatten()
            plt.plot(x, y4, marker='o', label='KL-UCB')
            y5 = rr3.values.flatten()
            plt.plot(x, y5, marker='o', label='Round-robin')
            y6 = ts3.values.flatten()
            plt.plot(x, y6, marker='o', label='Thomson-sampling')
            y7 = ucb3.values.flatten()
            plt.plot(x, y7, marker='o', label='UCB')
            plt.xlabel('Horizon')
            plt.ylabel('Regret')
            plt.title('instance-%d'%i)
            plt.legend()
            plt.savefig('instance%d.png'%i)
            plt.close()