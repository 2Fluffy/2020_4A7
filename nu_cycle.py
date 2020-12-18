import numpy as np
import matplotlib.pyplot as plt

gamma=1.4
theta = 6
nu_t = 0.9
nu_c=0.9

r = np.linspace(1,70,70)
nu_cycle_array=np.zeros(len(r))
x=1
while x < len(r):
    nu_cycle = (theta*(1-1/(r[x]**((gamma-1)/gamma)))*nu_t - (r[x]**((gamma-1)/gamma) - 1)/nu_c)/(theta-1-(r[x]**((gamma-1)/gamma)-1)/nu_c)
    nu_cycle_array[x]=nu_cycle
    x+=1

plt.plot(r,nu_cycle_array)
plt.xlabel('Pressure Ratio')
plt.ylabel('Cycle Efficiency')
plt.title('Cycle Efficiency vs Pressure Ratio')
plt.show()
