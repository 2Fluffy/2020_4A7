import pollutionanalysisloop as pal
import numpy as np
import matplotlib.pyplot as plt

#Function Constants
no_of_passengers=240
w_f = 74 #fuel weight
FPR = 1.45 # Fan Pressure ratio
theta  = 6 # turbine entry temp ratio, theta = t04/t02
nu_c = 0.9 # compressor efficiency
nu_t = 0.9 #turbine efficiency
#range = 11500
r = 45 # overall pressure ratio , r = p03/p02
stoichiometric_multiplier = 2
K_1 = 0.0125 # Parabolic Drag Law Constraints
K_2 = 0.0446 # Parabolic Drag Law Constraints
nu = 1

#Weight Constraints
w_mp = 40 #tonnes, maximum payload
w_e = 106 # tonnes, empty weight
w_p = 40
fuel_capacity_max = 74 # tonnes, @ max payload
w_mto = 220 #tonnes, max takeoff weight
range = 10000
array_length=21
flight_altitude_array = np.linspace(5,15,array_length)
data=np.zeros((array_length,6))
i=0
for altitude in flight_altitude_array:
    data[i] = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p)
    print(data[i,0])
    i+=1

fuel_burn_per_pass_km = np.zeros(array_length)
CO2_per_pass_km = np.zeros(array_length)
NOx_per_pass_km = np.zeros(array_length)
transonic_drag_array = np.zeros(array_length)
transonic_altitudes=np.array(0)
transonic_fuel=np.array(0)

j=0
while j< (len(data)):
    fuel_burn_per_pass_km[j]=data[j,2]
    transonic_drag_array[j]=data[j,5]
    j+=1

k=0
while k< (len(data)):

    if transonic_drag_array[k] == 1:
        transonic_altitudes = np.append(transonic_altitudes, flight_altitude_array[k])
        transonic_fuel = np.append(transonic_fuel, fuel_burn_per_pass_km[k])
    k+=1

try:
    b_transonic_altitudes = np.delete(transonic_altitudes, 0)
    b_transonic_fuel = np.delete(transonic_fuel,0)

except:
    print('No Transonic Drag')
print(b_transonic_fuel)
plt.plot(flight_altitude_array,fuel_burn_per_pass_km)
plt.plot(b_transonic_altitudes,b_transonic_fuel, '-r')
plt.xlabel('Range (m)')
plt.ylabel('Fuel Used Per Passenger Km')
plt.title('Fuel Used vs Range for Reference Data')
plt.show()
