import pollutionanalysisloop as pal

def min_fuel_finder(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p=None):

    fuel_used = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p)[0]
    while w_f-fuel_used>0 and fuel_used < 98.0:
            w_f-=0.1
            fuel_used = pal.pollutionanalysis(no_of_passengers,FPR,theta,nu_c,nu_t,range,r,stoichiometric_multiplier,K_1,K_2,altitude,w_f,nu,w_p)[0]



    return(w_f)
