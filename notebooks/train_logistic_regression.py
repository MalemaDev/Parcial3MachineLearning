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

# ======================================
#      CARGA OBLIGATORIA DEL DATASET
# ======================================

print("[INFO] Cargando dataset Telco Customer Churn...")

dataset_path = 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'

# Validar que el archivo exista
if not os.path.exists(dataset_path):
    raise FileNotFoundError(
        f"ERROR: No se encontró el archivo '{dataset_path}'. "
        "Debes colocarlo en la carpeta data/ para continuar."
    )

# Cargar archivo
df = pd.read_csv(dataset_path)

# Validación básica
if 'TotalCharges' not in df.columns or len(df) < 10:
    raise ValueError("ERROR: El dataset no es válido o está vacío.")


# ======================================
#          PREPROCESAMIENTO
# ======================================

print("[INFO] Preprocesando datos...")

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna(subset=['TotalCharges'])

categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('customerID')
categorical_cols.remove('Churn')

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Target
y = (df['Churn'] == 'Yes').astype(int)

# Features
X = df.drop(['customerID', 'Churn'], axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Escalado
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"[INFO] Dataset split: Train {X_train.shape[0]}, Test {X_test.shape[0]}")
print(f"[INFO] Features: {X.shape[1]}")

# ======================================
#     ENTRENAMIENTO REGRESIÓN LOGÍSTICA
# ======================================

print("\n[ENTRENANDO] Regresión Logística...")

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

# Predicciones
y_pred_lr = lr.predict(X_test_scaled)
y_pred_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]

# Métricas
lr_accuracy = accuracy_score(y_test, y_pred_lr)
lr_precision = precision_score(y_test, y_pred_lr)
lr_recall = recall_score(y_test, y_pred_lr)
lr_f1 = f1_score(y_test, y_pred_lr)
lr_auc = roc_auc_score(y_test, y_pred_proba_lr)
lr_cm = confusion_matrix(y_test, y_pred_lr)

print(f"\n[METRICAS] Regresión Logística:")
print(f"Accuracy: {lr_accuracy:.4f}")
print(f"Precision: {lr_precision:.4f}")
print(f"Recall: {lr_recall:.4f}")
print(f"F1-Score: {lr_f1:.4f}")
print(f"AUC: {lr_auc:.4f}")
print(f"Confusion Matrix:\n{lr_cm}")

# ======================================
#          GUARDADO DEL MODELO
# ======================================

print("\n[GUARDANDO] Modelo Logistic Regression...")
pickle.dump(lr, open('models/logistic_regression.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_lr.pkl', 'wb'))
pickle.dump(label_encoders, open('models/label_encoders.pkl', 'wb'))

# ======================================
#              GRÁFICAS
# ======================================

print("[GENERANDO] Gráficas...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# ROC Curve
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_proba_lr)
axes[0].plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC={lr_auc:.3f})', lw=2, color='#3b82f6')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve - Logistic Regression')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Confusion Matrix
sns.heatmap(lr_cm, annot=True, fmt='d', ax=axes[1], cmap='Blues')
axes[1].set_title('Confusion Matrix - Logistic Regression')
axes[1].set_ylabel('True Label')
axes[1].set_xlabel('Predicted Label')

plt.tight_layout()
plt.savefig('models/logistic_regression_metrics.png', dpi=150, bbox_inches='tight')
print("[OK] Gráficas guardadas en models/logistic_regression_metrics.png")

# ======================================
#              RESUMEN
# ======================================

with open('models/logistic_regression_summary.txt', 'w') as f:
    f.write("=== TELCO CUSTOMER CHURN - REGRESIÓN LOGÍSTICA ===\n\n")
    f.write(f"Accuracy: {lr_accuracy:.4f}\n")
    f.write(f"Precision: {lr_precision:.4f}\n")
    f.write(f"Recall: {lr_recall:.4f}\n")
    f.write(f"F1-Score: {lr_f1:.4f}\n")
    f.write(f"AUC-ROC: {lr_auc:.4f}\n")
    f.write(f"\nConfusion Matrix:\n{lr_cm}\n")

print("\n[EXITO] Entrenamiento Logistic Regression completado!")
