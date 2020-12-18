#Coursework for the Airplane Efficiency
import numpy as np
import math
import matplotlib.pyplot as plt

def pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,Flight_altitude,w_f,nu,w_p=None,w_e=106,stage_altitude_increase=None,altindex=None,):
    #Variables for routine


    #Reference Data
    max_passenger = 240
    range_max = 12000 #km, @ max paylaod
    w_mp = 40 #tonnes, maximum payload

    fuel_capacity_max = 74 # tonnes, @ max payload
    w_mto = 220 #tonnes, max takeoff weight
    S_wing_area=315 # wing area m^2
    T_a_sl=288 #temperature atmospheric @ sea level;
    p_a_sl=101 *10**3#pressure atmospheric @ sea level
    rho_sl = 1.225 #
    gamma=1.4
    R_gas=287
    g=9.81
    cp=1
    Stoichiometry = 15.1
    EI_co2=3088 # g/CO2 per kg fuel burn
    mass_passenger = 100
    if w_p == None:
        w_p = no_of_passengers*mass_passenger/1000

    ##Reference Engine @ Cruise Data
    nu_f = 0.92 # fan efficiency
    nu_tr = 0.9 #transfer efficiency
    LCV = 42.7*10**6 # LCV of Kerosene



    ##Modelling Constraints
    k = 0.015 #Fuel Burn Offset
    c_1 = 0.3 # aircraft weight correlation
    c_2 = 1 # aircraft weight correlation


    #Set Parameters

    B_star = 2*math.sqrt(K_1 * K_2)


    ## Generate ISA Lookup Table

    #set arrays
    h = np.linspace(0,20,801) # heights in km
    list_length=len(h)
    T = np.zeros(list_length)
    aa0 = np.zeros(list_length)
    pp0 = np.zeros(list_length)
    rhorho0 = np.zeros(list_length)

    # loop through altitudes

    i=0
    j=0
    while h[i]<=11:
        T[i]=288.15-6.5*h[i]
        pp0[i]=(T[i]/T[0])**5.256
        rhorho0[i]=(T[i]/T[0])**4.256
        rho0=rho_sl
        i += 1
    #reached troposphere, store values then loop through rest of altitude value
    p_Trop=pp0[i-1]
    rho_Trop=rhorho0[i-1]
    while i<list_length:
        T[i] = 216.65
        pp0[i] = math.exp(-0.1577*(h[i]-11)) * p_Trop
        rhorho0[i] = math.exp(-0.1577*(h[i]-11)) * rho_Trop
        i +=1

    a_0 = math.sqrt(gamma*R_gas*T[0])

    while j < list_length:
        aa0[j]=math.sqrt(gamma*R_gas*T[j])/a_0
        j+=1



    ##Flight Parameters
    w_to = w_e+w_p+w_f
    no_of_stages = 1
    stage_length = range/no_of_stages
    stage_altitude_increase=0
    s = 0
    transonic_drag_label = 0

    ## Determine Engine Core Cycle Efficiency

    nu_cycle = (theta*(1-1/(r**((gamma-1)/gamma)))*nu_t - (r**((gamma-1)/gamma) - 1)/nu_c)/(theta-1-(r**((gamma-1)/gamma)-1)/nu_c)
    EI_Nox_stages = np.zeros(no_of_stages)

    ## Main Loop
    loop_interation = 0
    while loop_interation < no_of_stages:

        try: altitude_array
        except NameError: altitude_array = None
        try: stage_altitude_increase
        except NameError: stage_altitude_increase = None

        if altitude_array != None:
            Flight_altitude = altitude_array[loop_interation]

        altindex = np.where(h==Flight_altitude) # index of current altitude in h array
        altindex=np.array(altindex)

        w_current=w_e + w_p + w_f
        current_wing_loading = w_current * 10**3* g / S_wing_area
        V_e_star = ((w_current*10**3*(9.81/(0.5*rho_sl*S_wing_area)))**0.5)*((K_2/K_1)**0.25) # Calculating Optimum EAS

        V_e = nu * V_e_star # Calculate Actual EAS from EAS ratio nu


        TAS = V_e / rhorho0[altindex]**0.5 # Calculate true air speed (TAS)
        M = TAS/(aa0[altindex]*a_0) # Calculate mach number
        if M>0.85: # Check if transonic drag
            print('Danger: Transonic Drag')
            transonic_drag_label=1


        #Calculate static pressures from lookup table
        T_a_c = T[altindex]
        p_a_c = pp0[altindex]*p_a_sl

        #calculate stagnation pressures from static pressures and TAS
        p_stag_c = p_a_c + (TAS**2)/(2*cp)
        t_stag_c = T_a_c + (TAS**2)/(2*cp*1000)

        #calculate T03
        t03=t_stag_c*(1+((r**((gamma-1)/gamma)-1)/nu_c))
        #calculate NOx

        EI_Nox = 0.011445*math.exp(0.00676593*t03)

        EI_Nox_stages[loop_interation] = EI_Nox

        M_j_squared = (2/(gamma-1))*(((FPR*p_stag_c/p_a_c)**((gamma-1)/gamma))-1) #using reference values for cruise conditions, change once calculating
        m_j = M_j_squared **0.5

        T_j=T_a_c* ((1+0.5*(gamma-1)*M**2)/(1+0.5*(gamma-1)*m_j**2))*FPR**((gamma-1)/(gamma*nu_f))
        nu_prop = 2*(1+(m_j/M) * math.sqrt(T_j/T_a_c))**(-1) # propulsive efficiency
        beta = 0.5*B_star*(nu**2+nu**(-2))
        LoverD=1/beta
        H = nu_prop * nu_cycle * nu_tr*LoverD*LCV/(g*1000)
        if loop_interation == 0:
            fuel_burn = w_to * (1-(math.exp(-stage_length/H))+k)
            w_f=w_f-fuel_burn

        else:

            fuel_burn =w_current - w_current/(math.exp(stage_length/H))
            w_f=w_f-fuel_burn

        s=s+stage_length


        if stage_altitude_increase != 0 & stage_altitude_increase != None:
            Flight_altitude = Flight_altitude + stage_altitude_increase

        loop_interation+=1

    ## Emissions Calculations

    fuel_used=w_to-w_e-w_p-w_f
    fuel_burn_per_km = fuel_used * 1000/s
    fuel_burn_per_payload_km = fuel_burn_per_km/(w_p*1000)
    fuel_burn_per_pass_km = fuel_burn_per_payload_km * mass_passenger
    CO2_per_pass_km = fuel_used/(s*w_p)*EI_co2*mass_passenger
    Av_EI_Nox = np.mean(EI_Nox_stages)
    NOx_per_pass_km = Av_EI_Nox*(fuel_used/(s*w_p))*Stoichiometry*stoichiometric_multiplier*mass_passenger

    return fuel_used,fuel_burn_per_km,fuel_burn_per_pass_km,CO2_per_pass_km,NOx_per_pass_km,transonic_drag_label
