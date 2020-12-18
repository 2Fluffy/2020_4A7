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
w_p = 24
range = 4000
array_length=56
no_of_altitudes = 8
pressure_ratio_array = np.linspace(5,60,array_length)
altitudes = np.linspace(5,12,no_of_altitudes)
data=np.zeros((no_of_altitudes,array_length,6))
x=0
i=0
for altitude in altitudes:
    for ratio in pressure_ratio_array:
        print(i)
        data[x,i] = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,ratio,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p)
        i+=1
    i=0
    x+=1

fuel_burn_per_pass_km = np.zeros((no_of_altitudes,array_length))
CO2_per_pass_km = np.zeros((no_of_altitudes,array_length))
NOx_per_pass_km = np.zeros((no_of_altitudes,array_length))
transonic_drag_array = np.zeros((no_of_altitudes,array_length))
transonic_PR=np.zeros((no_of_altitudes,1))
transonic_fuel=np.array((no_of_altitudes,1))
CO2_label_array = [None]*no_of_altitudes
NOx_label_array = [None]*no_of_altitudes

x=0
j=0
while x < no_of_altitudes:
    while j< array_length:
        fuel_burn_per_pass_km[x,j]=data[x,j,2]
        CO2_per_pass_km[x,j] = data[x,j,3]
        NOx_per_pass_km[x,j] = data[x,j,4]
        transonic_drag_array[x,j] = data[x,j,5]
        j+=1
    x+=1
    j=0
k=0
x=0
print(transonic_drag_array)
while k< array_length:

    if transonic_drag_array[x,k] == 1:
        transonic_PR[x] = np.append(transonic_PR[x], pressure_ratio_array[k])
        transonic_fuel[x] = np.append(transonic_fuel[x], fuel_burn_per_pass_km[k])
    k+=1

try:
    b_transonic_altitudes = np.delete(transonic_PR[x], 0)
    b_transonic_fuel = np.delete(transonic_fuel[x],0)

except:
    print('No Transonic Drag')

y=0
while y < no_of_altitudes:
    CO2_label_array[y] = 'CO2 at an altitude of ' + str(altitudes[y]) + 'km'
    NOx_label_array[y] = 'NOx at an altitude of ' + str(altitudes[y]) + 'km'
    y+=1

fig = plt.figure()
ax1 = fig.add_subplot(111)
x=0
while x < no_of_altitudes:
    ax1.plot(pressure_ratio_array,CO2_per_pass_km[x],label = CO2_label_array[x])
    ax1.set_ylabel('gCO2 / pass km')
    ax1.set_xlabel('Pressure Ratio')
    x+=1
x=0
ax2 = ax1.twinx()
ax2.set_ylabel('gNOx / pass km', color='r')
while x < no_of_altitudes:
    ax2.plot(pressure_ratio_array,NOx_per_pass_km[x],linestyle ='dashed',label = NOx_label_array[x])

    x+=1

ax1.legend()
ax2.legend()
plt.show()
