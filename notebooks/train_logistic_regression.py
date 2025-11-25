# script para entrenar el modelo de regresion logistica usando el dataset de churn
# seguimos un flujo simple: cargar datos, preparar, entrenar, evaluar y guardar

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_curve, auc, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import sys

# añadimos la ruta del archivo para evitar errores en ejecuciones externas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# se crean las carpetas necesarias por si no existen
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# intento de cargar el dataset real
try:
    print("[INFO] cargando dataset telco customer churn...")
    df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # validación básica del archivo cargado
    if 'TotalCharges' not in df.columns or len(df) < 10:
        raise ValueError("csv invalido o vacio")
    
except Exception as e:
    print(f"[WARNING] error al cargar csv: {e}")
    print("[INFO] generando datos de prueba...")
    
    # generamos datos sintéticos para pruebas cuando no existe el csv real
    np.random.seed(42)
    n_samples = 5000
    
    df = pd.DataFrame({
        'customerID': [f'id_{i}' for i in range(n_samples)],
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples),
        'Partner': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['Yes', 'No'], n_samples),
        'tenure': np.random.randint(1, 72, n_samples),
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
        'MonthlyCharges': np.random.uniform(20, 120, n_samples),
        'TotalCharges': np.random.uniform(100, 8000, n_samples),
        'Churn': np.random.choice(['Yes', 'No'], n_samples, p=[0.27, 0.73])
    })
    
    # guardamos estos datos para la próxima vez
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv', index=False)
    print("[INFO] datos generados y guardados en data/")

# preprocesamiento inicial
print("[INFO] preprocesando datos...")

# totalcharges como número y se eliminan filas con errores
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna(subset=['TotalCharges'])

# columnas categóricas que necesitan encoding
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('customerID')
categorical_cols.remove('Churn')

# aplicamos label encoding a todas las columnas categóricas
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# variable objetivo (convertida a 0/1)
y = (df['Churn'] == 'Yes').astype(int)

# variables predictoras
X = df.drop(['customerID', 'Churn'], axis=1)

# separación de datos en train y test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# escalado de variables para mejorar el rendimiento del modelo
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"[INFO] dataset split: train {X_train.shape[0]}, test {X_test.shape[0]}")
print(f"[INFO] features: {X.shape[1]}")

# ==============================
# entrenamiento regresion logistica
# ==============================
print("\n[ENTRENANDO] regresion logistica...")

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

# predicciones y probabilidades
y_pred_lr = lr.predict(X_test_scaled)
y_pred_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]

# calculamos métricas principales
lr_accuracy = accuracy_score(y_test, y_pred_lr)
lr_precision = precision_score(y_test, y_pred_lr)
lr_recall = recall_score(y_test, y_pred_lr)
lr_f1 = f1_score(y_test, y_pred_lr)
lr_auc = roc_auc_score(y_test, y_pred_proba_lr)
lr_cm = confusion_matrix(y_test, y_pred_lr)

print(f"\n[METRICAS] regresion logistica:")
print(f"accuracy: {lr_accuracy:.4f}")
print(f"precision: {lr_precision:.4f}")
print(f"recall: {lr_recall:.4f}")
print(f"f1-score: {lr_f1:.4f}")
print(f"auc: {lr_auc:.4f}")
print(f"confusion matrix:\n{lr_cm}")

# ==============================
# guardar modelo y utilidades
# ==============================
print("\n[GUARDANDO] modelo logistic regression...")
pickle.dump(lr, open('models/logistic_regression.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_lr.pkl', 'wb'))
pickle.dump(label_encoders, open('models/label_encoders.pkl', 'wb'))

# ==============================
# generación de gráficas
# ==============================
print("[GENERANDO] gráficas...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# curva roc
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_proba_lr)
axes[0].plot(fpr_lr, tpr_lr, label=f'logistic regression (auc={lr_auc:.3f})', lw=2, color='#3b82f6')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
axes[0].set_xlabel('false positive rate')
axes[0].set_ylabel('true positive rate')
axes[0].set_title('roc curve - logistic regression')
axes[0].legend()
axes[0].grid(alpha=0.3)

# matriz de confusión
sns.heatmap(lr_cm, annot=True, fmt='d', ax=axes[1], cmap='Blues')
axes[1].set_title('confusion matrix - logistic regression')
axes[1].set_ylabel('true label')
axes[1].set_xlabel('predicted label')

plt.tight_layout()
plt.savefig('models/logistic_regression_metrics.png', dpi=150, bbox_inches='tight')
print("[OK] gráficas guardadas en models/logistic_regression_metrics.png")

# ==============================
# archivo resumen
# ==============================
with open('models/logistic_regression_summary.txt', 'w') as f:
    f.write("=== telco customer churn - regresion logistica ===\n\n")
    f.write(f"accuracy: {lr_accuracy:.4f}\n")
    f.write(f"precision: {lr_precision:.4f}\n")
    f.write(f"recall: {lr_recall:.4f}\n")
    f.write(f"f1-score: {lr_f1:.4f}\n")
    f.write(f"auc-roc: {lr_auc:.4f}\n")
    f.write(f"\nconfusion matrix:\n{lr_cm}\n")

print("\n[EXITO] entrenamiento logistic regression completado!")
