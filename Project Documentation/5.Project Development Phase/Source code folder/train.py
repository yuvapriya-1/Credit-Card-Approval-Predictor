import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier

def train_model():
    # 1. Load and clean
    df = pd.read_csv('data/creditcard_data.csv')
    df.columns = df.columns.str.strip()
    if 'Target' in df.columns: df.rename(columns={'Target': 'Approved'}, inplace=True)
    if 'ID' in df.columns: df.drop(columns=['ID'], inplace=True)
    df = df.dropna()

    # 2. Balance classes (Fixes the "Always Rejected" problem)
    df_app = df[df['Approved'] == 1]
    df_rej = df[df['Approved'] == 0].sample(n=len(df_app), random_state=42)
    df = pd.concat([df_app, df_rej])

    # 3. Create features
    X = pd.get_dummies(df.drop(columns=['Approved']))
    y = df['Approved']

    # 4. Save the model and the features it expects
    os.makedirs('models', exist_ok=True)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, 'models/card_model.joblib')
    joblib.dump(X.columns.tolist(), 'models/feature_names.joblib')
    print("Training Complete. Model and feature blueprint saved.")

if __name__ == "__main__":
    train_model()