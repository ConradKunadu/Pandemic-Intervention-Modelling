import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Data provided
data = {
    "Mortality Rate": [0, 2333333/8000000000, 1],
    "Marginal Lives Saved Per Doctor Per Year": [0.68493151, 0.68504566, 5.43737769]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transforming both the GDP and Share of Value data using logarithms
X = df['Mortality Rate'].values.reshape(-1, 1)  # Reshape for sklearn
Y = np.log(df['Marginal Lives Saved Per Doctor Per Year']).values.reshape(-1, 1)  # Reshape for sklearn

# Creating and fitting the linear regression model
model = LinearRegression()
model.fit(X, Y)

# Extracting the slope (m) and intercept (c)
m = model.coef_[0]
c = model.intercept_

# Displaying the results
print("Slope (m):", m)
print("Intercept (c):", c)