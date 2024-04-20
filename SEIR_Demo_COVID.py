import numpy as np
import matplotlib.pyplot as plt

def seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days):
    S = N - E0 - I0 - R0
    E = E0
    I = I0
    R = R0
    
    S_vals = [S]
    E_vals = [E]
    I_vals = [I]
    R_vals = [R]
    H_vals = [I * 0.5]  # Assuming 50% hospitalization rate
    
    for _ in range(num_days - 1):
        new_infections = beta * I * S / N
        new_exposed = new_infections
        new_infectious = sigma * E
        new_recoveries = gamma * I
        
        S -= new_exposed
        E += new_exposed - new_infectious
        I += new_infectious - new_recoveries
        R += new_recoveries
        
        S_vals.append(S)
        E_vals.append(E)
        I_vals.append(I)    
        R_vals.append(R)
        H_vals.append(I * 0.5)
    
    return S_vals, E_vals, I_vals, R_vals, H_vals

# Model parameters
N = 1000  # Total population
R0 = 3.28  # Reproduction number (average of 15-20)
incubation_period = 7  # Incubation period (days)
infectious_period = 5  # Infectious period (days)
sigma = 1/incubation_period  # Incubation rate (1/incubation period)
gamma = 1/infectious_period  # Recovery rate (1/infectious period)
beta = R0 * gamma  # Transmission rate
E0 = 1  # Initial exposed individuals
I0 = 0  # Initial infected individuals
R0 = 0  # Initial recovered individuals
num_days = 100  # Number of days to simulate

# Run the SEIR model
S_vals, E_vals, I_vals, R_vals, H_vals = seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days)

# Find the date when hospitalizations crossed the threshold
threshold = 44
threshold_date = None
for i in range(num_days):
    if H_vals[i] > threshold:
        threshold_date = i
        break

# Plot the results
days = range(num_days)
plt.figure(figsize=(10, 6))
plt.plot(days, I_vals, label='Infected')
plt.plot(days, R_vals, label='Recovered')
plt.plot(days, H_vals, label='Hospitalized', linestyle='--')
plt.axhline(y=threshold, color='r', linestyle='-', label='Detection Threshold')
plt.xlabel('Days')
plt.ylabel('Number of Individuals')
plt.title('SEIR Model - COVID-19 Outbreak')
plt.legend()
plt.grid(True)

# Add the threshold date to the plot
if threshold_date is not None:
    plt.annotate(f'Threshold crossed on day {threshold_date}', xy=(threshold_date, threshold),
                 xytext=(threshold_date+5, threshold+100), arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.show()