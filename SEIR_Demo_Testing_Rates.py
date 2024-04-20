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

num_simulations = 1000  # Number of simulations to run
testing_rates = np.arange(0.001, 0.01, 0.001)  # Testing rates to evaluate

# Find the threshold day when hospitalizations crossed 44
threshold = 44
threshold_day = None
for i in range(num_days):
    S_vals, E_vals, I_vals, R_vals, H_vals, _ = seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days, 0)
    if H_vals[i] > threshold:
        threshold_day = i
        break

# Run simulations for different testing rates
beat_threshold_percentages = []
for testing_rate in testing_rates:
    beat_threshold_count = 0
    for _ in range(num_simulations):
        _, _, _, _, _, detection_day = seir_model(N, beta, sigma, gamma, E0, I0, R0, num_days, testing_rate)
        if detection_day is not None and detection_day < threshold_day:
            beat_threshold_count += 1
    beat_threshold_percentage = beat_threshold_count / num_simulations * 100
    beat_threshold_percentages.append(beat_threshold_percentage)
    print(f"Testing rate: {testing_rate:.8f}, Beat threshold percentage: {beat_threshold_percentage:.2f}%")

# Find the minimum testing rate needed to beat the threshold day with more than 95% chance
min_testing_rate = None
for i in range(len(testing_rates)):
    if beat_threshold_percentages[i] > 99:
        min_testing_rate = testing_rates[i]
        break

print(f"\nMinimum testing rate needed to beat the threshold day with more than 99% chance: {min_testing_rate:.2f}")

# Plot the beat threshold percentage vs testing rate
plt.figure(figsize=(8, 6))
plt.plot(testing_rates, beat_threshold_percentages, marker='o')
plt.xlabel('Testing Rate')
plt.ylabel('Beat Threshold Percentage')
plt.title('Beat Threshold Percentage vs Testing Rate')
plt.grid(True)
plt.show()