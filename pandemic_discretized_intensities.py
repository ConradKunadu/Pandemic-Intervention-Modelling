import numpy as np
import pandas as pd
from scipy.stats import genpareto

### Create GPD

## Parameters for the generalized Pareto distribution (GPD)
xi = 1.41  # Shape parameter (ξ)
sigma = 0.0113  # Scale parameter (σ)
mu_prime = 0.001  # Detectability threshold (μ')
alpha = 0.62  # Detectability probability constant (α)
mu_double_prime = 17.8  # Truncation threshold (μ'')

## Create the GPD object from scipy.stats
gpd = genpareto(c=xi, loc=mu_prime, scale=sigma)

## Percentiles from 1% to 99%
percentiles = np.linspace(0.01, 0.99, 99)

## Calculate intensity levels for each percentile
intensity_levels = gpd.ppf(percentiles) # Using the Percent Point Function (PPF), which is the inverse of the CDF
cdf_values = gpd.cdf(intensity_levels) # Calculate the CDF for each intensity level

### Creating DataFrame and saving.

## Create a DataFrame with the corrected values
percentile_intensity_df = pd.DataFrame({
    'Percentile': percentiles,
    'Intensity_Level': intensity_levels,
    'CDF_Value': cdf_values
})

## Save the DataFrame to a CSV file
csv_file_path = 'Percentiles_Final.csv'
percentile_intensity_df.to_csv(csv_file_path, index=False)

### Testing

## Calculate the intensity at a specific percentile
#percentile = 0.2916666667
#intensity = gpd.ppf(percentile)
#print(f"Intensity at {percentile}: {intensity}")

## Print the DataFrame
#print(percentile_intensity_df)


