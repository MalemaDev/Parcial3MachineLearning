# script para generar datos de prueba si no existen los csvs
import pandas as pd
import numpy as np
import os

os.makedirs('data', exist_ok=True)

# generar datos telco si no existen
if not os.path.exists('data/WA_Fn-UseC_-Telco-Customer-Churn.csv') or os.path.getsize('data/WA_Fn-UseC_-Telco-Customer-Churn.csv') < 100:
    print("[INFO] generando dataset telco de prueba...")
    
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'customerID': [f'customer_{i}' for i in range(n_samples)],
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples),
        'Tenure': np.random.randint(1, 72, n_samples),
        'PhoneService': np.random.choice(['Yes', 'No'], n_samples),
        'InternetService': np.random.choice(['Fiber optic', 'DSL', 'No'], n_samples),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'MonthlyCharges': np.random.uniform(20, 150, n_samples).round(2),
        'TotalCharges': np.random.uniform(20, 8600, n_samples).round(2),
        'Churn': np.random.choice(['Yes', 'No'], n_samples, p=[0.27, 0.73])
    }
    
    df_telco = pd.DataFrame(data)
    df_telco.to_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv', index=False)
    print("[OK] dataset telco guardado en data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# generar datos credit card si no existen
if not os.path.exists('data/CC-GENERAL.csv') or os.path.getsize('data/CC-GENERAL.csv') < 100:
    print("[INFO] generando dataset credit card de prueba...")
    
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'BALANCE': np.random.uniform(0, 10000, n_samples).round(2),
        'BALANCE_FREQUENCY': np.random.uniform(0, 1, n_samples).round(2),
        'PURCHASES': np.random.uniform(0, 30000, n_samples).round(2),
        'ONEOFF_PURCHASES': np.random.uniform(0, 50000, n_samples).round(2),
        'INSTALLMENT_PURCHASES': np.random.uniform(0, 30000, n_samples).round(2),
        'CASH_ADVANCE': np.random.uniform(0, 20000, n_samples).round(2),
        'PURCHASES_FREQUENCY': np.random.uniform(0, 1, n_samples).round(2),
        'ONEOFF_PURCHASES_FREQUENCY': np.random.uniform(0, 1, n_samples).round(2),
        'PURCHASES_INSTALLMENTS_FREQUENCY': np.random.uniform(0, 1, n_samples).round(2),
        'CASH_ADVANCE_FREQUENCY': np.random.uniform(0, 1, n_samples).round(2),
        'CASH_ADVANCE_TRX': np.random.randint(0, 100, n_samples),
        'PURCHASES_TRX': np.random.randint(0, 500, n_samples),
        'CREDIT_LIMIT': np.random.uniform(1000, 30000, n_samples).round(2),
        'PAYMENTS': np.random.uniform(0, 50000, n_samples).round(2),
        'MINIMUM_PAYMENTS': np.random.uniform(0, 10000, n_samples).round(2),
        'PRC_FULL_PAYMENT': np.random.uniform(0, 1, n_samples).round(2),
        'MONTHS_ON_BOOK': np.random.randint(1, 200, n_samples),
    }
    
    df_cc = pd.DataFrame(data)
    df_cc.to_csv('data/CC-GENERAL.csv', index=False)
    print("[OK] dataset credit card guardado en data/CC-GENERAL.csv")

print("\n[LISTO] Todos los datos están preparados!")
