import numpy as np
import matplotlib.pyplot as plt

gamma=1.4
theta = 6
nu_t = 0.9
nu_c=0.9
theta = np.linspace(3,8,6)
print(theta[0])
r = np.linspace(1,70,70)
nu_cycle_array=np.zeros((len(theta),len(r)))
x=1
y=0
while y < len(theta):
    while x < len(r):
        nu_cycle = (theta[y]*(1-1/(r[x]**((gamma-1)/gamma)))*nu_t - (r[x]**((gamma-1)/gamma) - 1)/nu_c)/(theta[y]-1-(r[x]**((gamma-1)/gamma)-1)/nu_c)
        nu_cycle_array[y,x]=nu_cycle
        x+=1
    y+=1
    x=0
plt.plot(r,nu_cycle_array[1],label = "theta = 4")
plt.plot(r,nu_cycle_array[2],label = "theta = 5")
plt.plot(r,nu_cycle_array[3],label = "theta = 6")
plt.plot(r,nu_cycle_array[4],label = "theta = 7")
plt.plot(r,nu_cycle_array[5],label = "theta = 8")
plt.xlabel('Pressure Ratio')
plt.ylabel('Cycle Efficiency')
plt.title('Cycle Efficiency vs Pressure Ratio')
plt.legend()
plt.ylim(bottom=0)
plt.grid(True)
plt.show()
