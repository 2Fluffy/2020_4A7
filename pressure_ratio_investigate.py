import pollutionanalysisloop as pal
import numpy as np
import matplotlib.pyplot as plt

#Function Constants
no_of_passengers=240
w_f = 90 #fuel weight
FPR = 1.45 # Fan Pressure ratio
theta  = 6 # turbine entry temp ratio, theta = t04/t02
nu_c = 0.9 # compressor efficiency
nu_t = 0.9 #turbine efficiency
range = 11500
r = 45 # overall pressure ratio , r = p03/p02
stoichiometric_multiplier = 2
K_1 = 0.0125 # Parabolic Drag Law Constraints
K_2 = 0.0446 # Parabolic Drag Law Constraints
nu = 1
altitude = 9.5
#Weight Constraints
w_mp = 40 #tonnes, maximum payload
w_e = 106 # tonnes, empty weight
fuel_capacity_max = 74 # tonnes, @ max payload
w_mto = 220 #tonnes, max takeoff weight
range = 10000
array_length=56
no_of_altitudes = 5
pressure_ratio_array = np.linspace(5,60,array_length)
altitudes = np.linspace(8,12,no_of_altitudes)
data=np.zeros((array_length,6))
i=0
for ratio in pressure_ratio_array:
    print(i)
    data[i] = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,ratio,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu)

    i+=1

fuel_burn_per_pass_km = np.zeros(array_length)
CO2_per_pass_km = np.zeros(array_length)
NOx_per_pass_km = np.zeros(array_length)
transonic_drag_array = np.zeros(array_length)
transonic_PR=np.array(0)
transonic_fuel=np.array(0)

j=0
while j< (len(data)):
    fuel_burn_per_pass_km[j]=data[j,2]
    CO2_per_pass_km[j] = data[j,3]
    NOx_per_pass_km[j] = data[j,4]
    j+=1

k=0
while k< (len(data)):

    if transonic_drag_array[k] == 1:
        transonic_PR = np.append(transonic_PR, pressure_ratio_array[k])
        transonic_fuel = np.append(transonic_fuel, fuel_burn_per_pass_km[k])
    k+=1

try:
    b_transonic_altitudes = np.delete(transonic_PR, 0)
    b_transonic_fuel = np.delete(transonic_fuel,0)

except:
    print('No Transonic Drag')
print(b_transonic_fuel)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(pressure_ratio_array,CO2_per_pass_km)
ax1.set_ylabel('CO2')
ax1.set_xlabel('Altitude (km)')
ax2 = ax1.twinx()
ax2.plot(pressure_ratio_array,NOx_per_pass_km, 'r-')
ax2.set_ylabel('NOx', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()
