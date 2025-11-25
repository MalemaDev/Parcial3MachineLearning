from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os
import traceback
import sys

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

os.makedirs('models', exist_ok=True)

def load_models():
    models = {}
    try:
        models['lr'] = pickle.load(open('models/logistic_regression.pkl', 'rb'))
        models['knn'] = pickle.load(open('models/knn.pkl', 'rb'))
        models['scaler'] = pickle.load(open('models/scaler.pkl', 'rb'))
        models['encoders'] = pickle.load(open('models/label_encoders.pkl', 'rb'))
        models['kmeans'] = pickle.load(open('models/kmeans.pkl', 'rb'))
        models['scaler_kmeans'] = pickle.load(open('models/scaler_kmeans.pkl', 'rb'))
        models['cluster_profiles'] = pickle.load(open('models/cluster_profiles.pkl', 'rb'))
        print("[OK] Todos los modelos cargados correctamente")
        return models
    except FileNotFoundError as e:
        print(f"[ERROR] No se encontraron los modelos: {e}")
        print("[INFO] Ejecuta primero los scripts de entrenamiento:")
        print("  python notebooks/train_logistic_regression.py")
        print("  python notebooks/train_knn.py")
        print("  python notebooks/train_kmeans.py")
        return {}

models = load_models()

@app.route('/health', methods=['GET'])
def health():
    """Verificar que el servidor está activo"""
    return jsonify({
        'status': 'OK',
        'models_loaded': all(k in models for k in ['lr', 'knn', 'kmeans'])
    }), 200

@app.route('/api/predict-churn-lr', methods=['POST', 'OPTIONS'])
def predict_churn_lr():
    """Predicción de Churn usando Regresión Logística"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        if 'lr' not in models or not models['lr']:
            return jsonify({'error': 'Modelos no cargados. Ejecuta los scripts de entrenamiento.'}), 500
            
        data = request.json
        
        categorical_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 
                               'PhoneService', 'MultipleLines', 'InternetService',
                               'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                               'TechSupport', 'StreamingTV', 'StreamingMovies',
                               'Contract', 'PaperlessBilling', 'PaymentMethod']
        numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
        
        encoded_data = {}
        for col in categorical_features:
            try:
                le = models['encoders'][col]
                val = data[col]
                if val == "Masculino":
                    val = "Male"
                elif val == "Femenino":
                    val = "Female"
                elif val == "Sí":
                    val = "Yes"
                elif val == "No":
                    val = "No"
                elif val == "Mes a mes":
                    val = "Month-to-month"
                elif val == "Cheque electrónico":
                    val = "Electronic check"
                
                encoded_data[col] = le.transform([val])[0]
            except (KeyError, ValueError):
                encoded_data[col] = 0
        
        for col in numerical_features:
            encoded_data[col] = float(data.get(col, 0))
        
        feature_order = categorical_features + numerical_features
        X_input = np.array([[encoded_data[col] for col in feature_order]])
        
        X_scaled = models['scaler'].transform(X_input)
        
        lr_pred = models['lr'].predict(X_scaled)[0]
        lr_proba = models['lr'].predict_proba(X_scaled)[0]
        
        return jsonify({
            'prediction': 1 if lr_pred == 1 else 0,
            'probability': float(lr_proba[1])
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict-churn-knn', methods=['POST', 'OPTIONS'])
def predict_churn_knn():
    """Predicción de Churn usando K-Nearest Neighbors"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        if 'knn' not in models or not models['knn']:
            return jsonify({'error': 'Modelos no cargados. Ejecuta los scripts de entrenamiento.'}), 500
            
        data = request.json
        
        categorical_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 
                               'PhoneService', 'MultipleLines', 'InternetService',
                               'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                               'TechSupport', 'StreamingTV', 'StreamingMovies',
                               'Contract', 'PaperlessBilling', 'PaymentMethod']
        numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
        
        encoded_data = {}
        for col in categorical_features:
            try:
                le = models['encoders'][col]
                val = data[col]
                if val == "Masculino":
                    val = "Male"
                elif val == "Femenino":
                    val = "Female"
                elif val == "Sí":
                    val = "Yes"
                elif val == "No":
                    val = "No"
                elif val == "Mes a mes":
                    val = "Month-to-month"
                elif val == "Cheque electrónico":
                    val = "Electronic check"
                
                encoded_data[col] = le.transform([val])[0]
            except (KeyError, ValueError):
                encoded_data[col] = 0
        
        for col in numerical_features:
            encoded_data[col] = float(data.get(col, 0))
        
        feature_order = categorical_features + numerical_features
        X_input = np.array([[encoded_data[col] for col in feature_order]])
        
        X_scaled = models['scaler'].transform(X_input)
        
        knn_pred = models['knn'].predict(X_scaled)[0]
        
        return jsonify({
            'prediction': 1 if knn_pred == 1 else 0
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict-cluster', methods=['POST', 'OPTIONS'])
def predict_cluster():
    """Predicción de Cluster usando K-Means"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        if 'kmeans' not in models or not models['kmeans']:
            return jsonify({'error': 'Modelos no cargados. Ejecuta los scripts de entrenamiento.'}), 500
            
        data = request.json
        
        features = ['BALANCE', 'BALANCE_FREQUENCY', 'PURCHASES', 'ONEOFF_PURCHASES',
                   'INSTALLMENTS_PURCHASES', 'CASH_ADVANCE', 'PURCHASES_FREQUENCY',
                   'ONEOFF_PURCHASES_FREQUENCY', 'PURCHASES_INSTALLMENTS_FREQUENCY',
                   'CASH_ADVANCE_FREQUENCY', 'CASH_ADVANCE_TRX', 'PURCHASES_TRX',
                   'CREDIT_LIMIT', 'PAYMENTS', 'MINIMUM_PAYMENTS', 'PRC_FULL_PAYMENT', 'TENURE']
        
        X_input = np.array([[float(data.get(col, 0)) for col in features]])
        
        X_scaled = models['scaler_kmeans'].transform(X_input)
        
        cluster_pred = models['kmeans'].predict(X_scaled)[0]
        
        profiles = models['cluster_profiles']
        profile_mean = profiles[cluster_pred]
        
        description = generate_cluster_description(cluster_pred, profile_mean)
        
        return jsonify({
            'cluster': int(cluster_pred),
            'profile_description': description
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

def generate_cluster_description(cluster_id, profile):
    """Generar descripción interpretable del cluster"""
    descriptions = {
        0: "Clientes con bajo uso - Balance bajo, pocas compras, crédito limitado",
        1: "Clientes activos - Balance moderado, compras regulares, buen crédito",
        2: "Clientes premium - Balance alto, muchas compras, crédito elevado"
    }
    return descriptions.get(cluster_id, "Cluster desconocido")

if __name__ == '__main__':
    print("[INFO] Iniciando servidor Flask en http://localhost:5000")
    print("[INFO] Asegúrate de haber entrenado los modelos primero")
    app.run(debug=True, port=5000, host='0.0.0.0')
