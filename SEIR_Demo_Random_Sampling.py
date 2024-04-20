import numpy as np
import matplotlib.pyplot as plt

def seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days, testing_rate):
    S = N - E0 - I0 - R0
    E = E0
    I = I0
    R = R0
    
    S_vals = [S]
    E_vals = [E]
    I_vals = [I]
    R_vals = [R]
    H_vals = [I * 0.2]  # Assuming 20% hospitalization rate
    
    detection_day = None
    for day in range(num_days - 1):
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
        H_vals.append(I * 0.2)
        
        # Perform random testing
        num_tests = int(testing_rate * N)
        if num_tests > 0:
            tested_individuals = np.random.choice(N, num_tests, replace=False)
            if any(tested_individuals < I) and detection_day is None:
                detection_day = day
    
    return S_vals, E_vals, I_vals, R_vals, H_vals, detection_day

# Model parameters
N = 1000  # Total population
R0 = 20  # Reproduction number (average of 15-20)
incubation_period = 10  # Incubation period (days)
infectious_period = 12  # Infectious period (days)
sigma = 1/incubation_period  # Incubation rate (1/incubation period)
gamma = 1/infectious_period  # Recovery rate (1/infectious period)
beta = R0 * gamma  # Transmission rate
E0 = 1  # Initial exposed individuals
I0 = 0  # Initial infected individuals
R0 = 0  # Initial recovered individuals
num_days = 50  # Number of days to simulate
testing_rate = 0.01  # Proportion of population randomly tested each day

num_simulations = 1000  # Number of simulations to run
detection_days = []  # List to store detection days from each simulation

# Run multiple simulations
for _ in range(num_simulations):
    S_vals, E_vals, I_vals, R_vals, H_vals, detection_day = seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days, testing_rate)
    if detection_day is not None:
        detection_days.append(detection_day)

# Calculate the mean detection day
mean_detection_day = np.mean(detection_days)

# Find the threshold day when hospitalizations crossed 44
threshold = 44
threshold_day = None
for i in range(num_days):
    if H_vals[i] > threshold:
        threshold_day = i
        break

# Plot the results
days = range(num_days)
plt.figure(figsize=(10, 6))
plt.plot(days, I_vals, label='Infected')
plt.plot(days, R_vals, label='Recovered')
plt.plot(days, H_vals, label='Hospitalized', linestyle='--')

# Add the threshold line to the plot
if threshold_day is not None:
    plt.axhline(y=threshold, color='r', linestyle='-', label='Detection Threshold')

# Add the mean detection day line to the plot
plt.axvline(x=mean_detection_day, color='g', linestyle='--', label='Mean Detection Day')

plt.xlabel('Days')
plt.ylabel('Number of Individuals')
plt.title(f'SEIR Model - Measles Outbreak w/ {testing_rate*100}% Random Testing')
plt.legend()
plt.grid(True)

# Add the threshold day label to the plot
if threshold_day is not None:
    plt.annotate(f'Threshold crossed on day {threshold_day}', xy=(threshold_day, threshold),
                 xytext=(threshold_day+1, threshold-20), arrowprops=dict(facecolor='black', arrowstyle='->'))

# Add the mean detection day label to the plot
plt.annotate(f'Mean Detection Day: {mean_detection_day:.2f}', xy=(mean_detection_day, I_vals[int(mean_detection_day)]),
             xytext=(mean_detection_day+1, I_vals[int(mean_detection_day)]+50),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.show()