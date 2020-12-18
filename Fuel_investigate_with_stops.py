import pollutionanalysisloop as pal
import numpy as np
import matplotlib.pyplot as plt
import minfuelfinder as mff

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
range = 12000

flight_altitude_array = [5,9,10]
array_length=len(flight_altitude_array)
no_of_stages=np.linspace(1,5,5)
stage_array_length = len(no_of_stages)
data=np.zeros((array_length,stage_array_length,6))
i=0
j=0
for altitude in flight_altitude_array:
    for stage in no_of_stages:
        w_f = mff.min_fuel_finder(no_of_passengers, FPR, theta, nu_c, nu_t, (range/stage), r, stoichiometric_multiplier, K_1, K_2, altitude, w_f, nu,w_p)
        data[i,j] = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,(range/stage),r,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p)
        print(j)
        print(data[i,j,0])
        j+=1
        w_f=74
    j=0
    i+=1
    print(i)

fuel_burn_per_pass_km = np.zeros((array_length,stage_array_length))
CO2_per_pass_km = np.zeros((array_length,stage_array_length))
NOx_per_pass_km = np.zeros((array_length,stage_array_length))
transonic_drag_array = np.zeros((array_length,stage_array_length))
transonic_altitudes=np.array(0)
transonic_fuel=np.array(0)
i=0
j=0
while i<array_length:
    while j< stage_array_length:
        fuel_burn_per_pass_km[i,j]=data[i,j,2]
        transonic_drag_array[i,j]=data[i,j,5]
        j+=1
    j=0
    i+=1

labels = ['0', '1', '2', '3', '4']


x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, fuel_burn_per_pass_km[0], width, label='Altitude = 5km')
rects2 = ax.bar(x, fuel_burn_per_pass_km[1], width, label='Altitude = 9km')
rects3 = ax.bar(x + width, fuel_burn_per_pass_km[2], width, label='Altitude = 10km')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Fuel Burn per Passenger km')
ax.set_xlabel('No of Refuelling Stops')
ax.set_title('Fuel Burn per Passenger km vs No of Stops for a 12000km Route')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height=rect.get_height()
        rounded_height = np.round(rect.get_height(),4)
        ax.annotate('{}'.format(rounded_height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()
plt.ylim(bottom=0.0125)
plt.show()
