# script para entrenar el modelo knn usando el dataset de churn de telco
# seguimos el flujo estándar: cargar datos, preparar, entrenar y guardar resultados

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    roc_curve, auc, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

# mensaje inicial del entrenamiento
print("[ENTRENANDO] K-Nearest Neighbors...")

# creamos carpetas necesarias por si no existen
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# ======================================
#     CARGA OBLIGATORIA DEL DATASET
# ======================================

print("[INFO] Cargando dataset Telco Customer Churn...")

dataset_path = 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'

# Validar existencia del archivo
if not os.path.exists(dataset_path):
    raise FileNotFoundError(
        f"ERROR: No se encontró el archivo '{dataset_path}'. "
        "Debes colocarlo en la carpeta data/ para continuar."
    )

# Cargar archivo real
df = pd.read_csv(dataset_path)

# Validar columnas mínimas
if 'TotalCharges' not in df.columns or len(df) < 10:
    raise ValueError("ERROR: El dataset no es válido o está vacío.")

# ======================================
#           PREPROCESAMIENTO
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

y = (df['Churn'] == 'Yes').astype(int)
X = df.drop(['customerID', 'Churn'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"[INFO] Dataset split: train {X_train.shape[0]}, test {X_test.shape[0]}")
print(f"[INFO] Features: {X.shape[1]}")

# ======================================
#           ENTRENAMIENTO KNN
# ======================================

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

y_pred_knn = knn.predict(X_test_scaled)
y_pred_proba_knn = knn.predict_proba(X_test_scaled)[:, 1]

# ======================================
#              MÉTRICAS
# ======================================

knn_accuracy = accuracy_score(y_test, y_pred_knn)
knn_precision = precision_score(y_test, y_pred_knn)
knn_recall = recall_score(y_test, y_pred_knn)
knn_f1 = f1_score(y_test, y_pred_knn)
knn_auc = roc_auc_score(y_test, y_pred_proba_knn)
knn_cm = confusion_matrix(y_test, y_pred_knn)

print(f"\n[METRICAS] K-Nearest Neighbors:")
print(f"Accuracy: {knn_accuracy:.4f}")
print(f"Precision: {knn_precision:.4f}")
print(f"Recall: {knn_recall:.4f}")
print(f"F1-Score: {knn_f1:.4f}")
print(f"AUC: {knn_auc:.4f}")
print(f"Confusion Matrix:\n{knn_cm}")

# ======================================
#         GUARDAR MODELO
# ======================================

print("\n[GUARDANDO] Modelo KNN...")
pickle.dump(knn, open('models/knn.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_knn.pkl', 'wb'))
pickle.dump(label_encoders, open('models/label_encoders.pkl', 'wb'))

# ======================================
#              GRÁFICAS
# ======================================

print("[GENERANDO] Gráficas...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

fpr_knn, tpr_knn, _ = roc_curve(y_test, y_pred_proba_knn)
axes[0].plot(fpr_knn, tpr_knn, label=f"KNN (AUC={knn_auc:.3f})", lw=2, color='#10b981')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve - KNN')
axes[0].legend()
axes[0].grid(alpha=0.3)

sns.heatmap(knn_cm, annot=True, fmt='d', ax=axes[1], cmap='Greens')
axes[1].set_title('Confusion Matrix - KNN')
axes[1].set_ylabel('True Label')
axes[1].set_xlabel('Predicted Label')

plt.tight_layout()
plt.savefig('models/knn_metrics.png', dpi=150, bbox_inches='tight')
print("[OK] Gráficas guardadas en models/knn_metrics.png")

# ======================================
#          RESUMEN DEL MODELO
# ======================================

with open('models/knn_summary.txt', 'w') as f:
    f.write("=== TELCO CUSTOMER CHURN - K-NEAREST NEIGHBORS ===\n\n")
    f.write(f"Accuracy: {knn_accuracy:.4f}\n")
    f.write(f"Precision: {knn_precision:.4f}\n")
    f.write(f"Recall: {knn_recall:.4f}\n")
    f.write(f"F1-Score: {knn_f1:.4f}\n")
    f.write(f"AUC-ROC: {knn_auc:.4f}\n")
    f.write(f"\nConfusion Matrix:\n{knn_cm}\n")

print("\n[EXITO] Entrenamiento KNN completado!")
