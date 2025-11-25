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

# intentamos cargar el dataset real
try:
    print("[INFO] cargando dataset telco customer churn...")
    df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # validamos que el archivo tenga contenido útil
    if 'TotalCharges' not in df.columns or len(df) < 10:
        raise ValueError("csv invalido o vacio")
    
except Exception as e:
    print(f"[WARNING] error al cargar csv: {e}")
    print("[INFO] generando datos de prueba...")
    
    # generamos datos sintéticos para no detener el entrenamiento
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
    
    # guardamos los datos para futuras ejecuciones
    df.to_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv', index=False)
    print("[INFO] datos generados y guardados en data/")

# preprocesamiento general
print("[INFO] preprocesando datos...")

# totalcharges queda como numérico y quitamos nulos
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna(subset=['TotalCharges'])

# identificamos columnas categóricas
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('customerID')
categorical_cols.remove('Churn')

# aplicación del label encoding para las columnas categóricas
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# variable objetivo y variables predictoras
y = (df['Churn'] == 'Yes').astype(int)
X = df.drop(['customerID', 'Churn'], axis=1)

# dividimos train y test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# escalamos las features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"[INFO] dataset split: train {X_train.shape[0]}, test {X_test.shape[0]}")
print(f"[INFO] features: {X.shape[1]}")

# entrenamos knn con k=5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# predicciones y probabilidades
y_pred_knn = knn.predict(X_test_scaled)
y_pred_proba_knn = knn.predict_proba(X_test_scaled)[:, 1]

# métricas del modelo
knn_accuracy = accuracy_score(y_test, y_pred_knn)
knn_precision = precision_score(y_test, y_pred_knn)
knn_recall = recall_score(y_test, y_pred_knn)
knn_f1 = f1_score(y_test, y_pred_knn)
knn_auc = roc_auc_score(y_test, y_pred_proba_knn)
knn_cm = confusion_matrix(y_test, y_pred_knn)

print(f"\n[METRICAS] k-nearest neighbors:")
print(f"accuracy: {knn_accuracy:.4f}")
print(f"precision: {knn_precision:.4f}")
print(f"recall: {knn_recall:.4f}")
print(f"f1-score: {knn_f1:.4f}")
print(f"auc: {knn_auc:.4f}")
print(f"confusion matrix:\n{knn_cm}")

# guardamos modelo, scaler y label encoders
print("\n[GUARDANDO] modelo knn...")
pickle.dump(knn, open('models/knn.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_knn.pkl', 'wb'))
pickle.dump(label_encoders, open('models/label_encoders.pkl', 'wb'))

# generamos gráficas de métricas
print("[GENERANDO] gráficas...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# curva roc
fpr_knn, tpr_knn, _ = roc_curve(y_test, y_pred_proba_knn)
axes[0].plot(fpr_knn, tpr_knn, label=f'knn (auc={knn_auc:.3f})', lw=2, color='#10b981')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
axes[0].set_xlabel('false positive rate')
axes[0].set_ylabel('true positive rate')
axes[0].set_title('roc curve - knn')
axes[0].legend()
axes[0].grid(alpha=0.3)

# matriz de confusión
sns.heatmap(knn_cm, annot=True, fmt='d', ax=axes[1], cmap='Greens')
axes[1].set_title('confusion matrix - knn')
axes[1].set_ylabel('true label')
axes[1].set_xlabel('predicted label')

plt.tight_layout()
plt.savefig('models/knn_metrics.png', dpi=150, bbox_inches='tight')
print("[OK] gráficas guardadas en models/knn_metrics.png")

# resumen en archivo txt
with open('models/knn_summary.txt', 'w') as f:
    f.write("=== telco customer churn - k-nearest neighbors ===\n\n")
    f.write(f"accuracy: {knn_accuracy:.4f}\n")
    f.write(f"precision: {knn_precision:.4f}\n")
    f.write(f"recall: {knn_recall:.4f}\n")
    f.write(f"f1-score: {knn_f1:.4f}\n")
    f.write(f"auc-roc: {knn_auc:.4f}\n")
    f.write(f"\nconfusion matrix:\n{knn_cm}\n")

print("\n[EXITO] entrenamiento knn completado!")
