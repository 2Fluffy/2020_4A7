import pollutionanalysisloop as pal
import numpy as np
import matplotlib.pyplot as plt

#Function Constants
no_of_passengers=200
w_f = 10 #fuel weight
FPR = 1.45 # Fan Pressure ratio
theta  = 6 # turbine entry temp ratio, theta = t04/t02
nu_c = 0.9 # compressor efficiency
nu_t = 0.9 #turbine efficiency
#range = 11500
r = 45 # overall pressure ratio , r = p03/p02
stoichiometric_multiplier = 2
K_1 = 0.0125 # Parabolic Drag Law Constraints
K_2 = 0.0446 # Parabolic Drag Law Constraints
Flight_altitude = 9.5
nu = 1

#Weight Constraints
w_mp = 40 #tonnes, maximum payload
w_e = 106 # tonnes, empty weight
fuel_capacity_max = 74 # tonnes, @ max payload
w_mto = 220 #tonnes, max takeoff weight
w_p=w_mp
range_array=np.array(0)
wp_array=np.array(40)

w_p = w_mp
range = 10
while w_p >0:

    while (w_e+w_f+w_p) <= w_mto:
        fuel_used = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,Flight_altitude,w_f,nu,w_p)[0]
        if fuel_used > w_f:
            w_f +=0.1
        else:
            range_array = np.append(range_array, range)
            wp_array=np.append(wp_array, w_p)
            range += 10
        print(range)
    #if label==True:
    #     w_p-=0.1
    #     w_f+=0.1
    #     label=False
    fuel_used = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,Flight_altitude,w_f,nu,w_p)[0]
    if w_f-fuel_used<0:
            w_p-=0.1
            w_f+=0.1
            try:
                fuel_used = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,Flight_altitude,w_f,nu,w_p)[0]
            except:
                range_array = np.append(range_array, range)
                wp_array=np.append(wp_array, 0)

    range_array = np.append(range_array, range)
    wp_array=np.append(wp_array, w_p)
    range += 10
    print(range)
i=0
lastwp=40
while i < len(wp_array):
    wp=wp_array[i]
    if wp==lastwp:
        index = i
        lastwp=wp
    i+=1
print(range_array[index])
plt.plot(range_array,wp_array,label = "Reference Data")
plt.plot([range_array[index],range_array[index]],[0,41],'r-',label = "Design Point")
plt.xlabel('Range (m)')
plt.ylabel('Payload (Tonnes)')
plt.title('Payload vs Range for Reference Data')
plt.legend()
plt.grid(True)
plt.show()
