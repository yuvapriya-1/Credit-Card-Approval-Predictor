from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and feature blueprint
model = joblib.load('models/card_model.joblib')
EXPECTED_FEATURES = joblib.load('models/feature_names.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # --- NEW: HARD BUSINESS RULES ---
        income = float(data.get('income', 0))
        years = float(data.get('years_employed', 0))
        
        if income < 10000:
            return jsonify({'approved': False, 'risk_level': 'High Risk (Invalid Income)'})
        if years < 3:
            return jsonify({'approved': False, 'risk_level': 'High Risk (Invalid Employment)'})
        # --------------------------------

        input_dict = {
            'gender': int(data.get('gender', 0)),
            'age': float(data.get('age', 30)),
            'income': income,
            'years_employed': years,
            'income_type': data.get('income_type'),
            'education': data.get('education'),
            'own_car': int(data.get('own_car', 0)),
            'own_property': int(data.get('own_property', 0))
        }

        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])
        
        # Create dummies and align with training columns
        df_encoded = pd.get_dummies(input_df)
        final_df = df_encoded.reindex(columns=EXPECTED_FEATURES, fill_value=0)

        # Check what the model actually sees
        print("DEBUG: Final DataFrame for Prediction:")
        print(final_df)
        print("DEBUG: Probability before threshold:", model.predict_proba(final_df)[0][1])
        # Predict
        prob = model.predict_proba(final_df)[0][1]
        
        is_approved = prob >= 0.20
        risk = "Low Risk" if prob >= 0.15 else ("Moderate Risk" if prob >= 0.12 else "High Risk")
        
        return jsonify({'approved': bool(is_approved), 'risk_level': risk})

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)