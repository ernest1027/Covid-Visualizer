import pandas as pd
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#beta = effective_contact_rate
#gamma = recovery_rate
#delta = death_rate
#alpha = vaccination_rate
#sigma = vaccination_effectiveness_rate
def deriv(state, t, N, beta, gamma, delta, alpha):
    S = state[0]
    I = state[1]
    V = state[4]

    dSdt = (-beta * S * I / N - alpha) if S >0 else 0  
    dIdt = beta * S * I / N - gamma * I  
    dRdt = gamma * I * (1-delta)
    dDdt = gamma * I * delta
    dVdt = alpha 
    return dSdt, dIdt, dRdt, dDdt,dVdt


total_pop = 1000
recovered = 0
infected = 1
susceptible = total_pop - infected - recovered
dead = 0
vaccinated = 0

transmission_rate = 0.05
contacts_per_day = 5
death_rate = 0.05
effective_contact_rate = transmission_rate*contacts_per_day
recovery_rate = 1/14
vaccination_rate = 10



days = range(0,160)

ret = odeint(deriv,[susceptible,infected,recovered,dead,vaccinated],days,args=(total_pop,effective_contact_rate,recovery_rate,death_rate,vaccination_rate))
S,I,R,D,V = ret.T

df = pd.DataFrame({
    'susceptible': S,
    'infected': I,
    'recovered': R,
    'dead' : D,
    'vaccinated': V,
    'day': days
})

print(df)

