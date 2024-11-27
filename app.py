from flask import Flask, request, jsonify
from flask_cors import CORS   
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the request data
        data = request.get_json()       
        make = data.get('make')
        model_name = data.get('model')
        year = int(data.get('year'))
        mileage = float(data.get('mileage'))
        fuel_type = data.get('fuel-type')  # Added fuel type
        owner_type = data.get('owner-type')  # Added owner type

        # Feature extraction (example of how to handle the new fields)
        # Feature array example: [year, mileage, fuel_type, owner_type, other features...]
        
        # Mapping categorical values to numerical for the model
        fuel_type_map = {'Petrol': 0, 'Diesel': 1}
        owner_type_map = {'First': 0, 'Second': 1, 'Third': 2, 'Fourth & Above': 3}

        # Ensure the inputs are valid
        fuel_type_value = fuel_type_map.get(fuel_type, 0)  # Default to 0 if invalid
        owner_type_value = owner_type_map.get(owner_type, 0)  # Default to 0 if invalid

        # Define the features based on the inputs
        features = [
            year,          # Year of manufacture
            mileage,       # Mileage
            fuel_type_value,  # Fuel Type (0 for Petrol, 1 for Diesel)
            owner_type_value,  # Owner Type (0 for First, 1 for Second, etc.)
            0,              # Placeholder for other features (adjust according to your model)
            15.0,           # Placeholder for other features like mileage-related values
            1500.0,         # Placeholder for engine size or similar features
            90.0,           # Placeholder for power (e.g., engine power in horsepower)
            5,              # Placeholder for number of seats
            0.0             # Placeholder for other car-related features
        ]

        # Convert to numpy array for model prediction
        inputs = np.array([features])
        
        # Get the prediction from the model
        prediction = model.predict(inputs)
        
        # Return the predicted price as a JSON response
        return jsonify({'predicted_price': round(prediction[0], 2)})

    except Exception as e:
        return jsonify({'error': f"Failed to fetch prediction: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
