import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Load dataset
data = pd.read_csv('car_prices.csv')

# Drop rows where the target variable (Price) is missing
data = data.dropna(subset=['Price'])

# Fill missing values for other columns
data['Engine'] = data['Engine'].fillna('Unknown')
data['Power'] = data['Power'].fillna('Unknown')
data['Seats'] = data['Seats'].fillna(data['Seats'].mode()[0])
data['New_Price'] = data['New_Price'].fillna('Unknown')

# Convert categorical columns to numeric values (simplified encoding)
data['Fuel_Type'] = data['Fuel_Type'].astype('category').cat.codes
data['Transmission'] = data['Transmission'].astype('category').cat.codes
data['Owner_Type'] = data['Owner_Type'].astype('category').cat.codes

# Extract numeric values from strings
data['Mileage'] = data['Mileage'].str.extract('(\d+\.\d+|\d+)').astype(float)
data['Engine'] = data['Engine'].str.extract('(\d+)').astype(float)
data['Power'] = data['Power'].str.extract('(\d+\.\d+|\d+)').astype(float)

# Drop irrelevant columns
data = data.drop(['Name', 'Location', 'New_Price'], axis=1)

# Features and target
X = data.drop('Price', axis=1)
y = data['Price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as 'model.pkl'")

