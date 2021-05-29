import pandas as pd
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#beta = effective_contact_rate
#gamma = recovery_rate
#delta = death_rate
#alpha = vaccination_rate
#sigma = vaccination_effectiveness_rate
def deriv(state, t, N, beta, gamma, delta, alpha, sigma):
    S = state[0]
    I = state[1]
    R = state[2]

    if(S<0):
        alpha = 0
    dSdt = (-beta * S * I / N) - alpha  
    dIdt = beta * S * I / N - (gamma * I) +  (R*sigma*beta*I/N)
    dRdt = gamma * I * (1-delta) + alpha  - (R*sigma*beta*I/N)
    dDdt = gamma * I * delta
    return dSdt, dIdt, dRdt, dDdt

total_pop = 15000000
recovered = 0
infected = 1
susceptible = total_pop - infected - recovered
dead = 0

transmission_rate = 0.05
contacts_per_day = 5
death_rate = 0.05
effective_contact_rate = 0.15
recovery_rate = 1/14
vaccination_rate = 0
vaccination_effectiveness_rate = 0.95


days = range(0,160)

ret = odeint(deriv,[susceptible,infected,recovered,dead],days,args=(total_pop,effective_contact_rate,recovery_rate,death_rate,vaccination_rate,vaccination_effectiveness_rate))
S,I,R,D = ret.T

def data_frame():

    df = pd.DataFrame({
        'susceptible': S,
        'infected': I,
        'recovered': R,
        'dead' : D,
        'day': days
    })

    return df

if __name__ == '__main__':
    print(df)
