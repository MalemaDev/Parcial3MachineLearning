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

# solo entrena el modelo knn
print("[ENTRENANDO] K-Nearest Neighbors...")

os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# intentar cargar el csv, si falla generar datos
try:
    print("[INFO] Cargando dataset Telco Customer Churn...")
    df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # verificar que tenga las columnas correctas
    if 'TotalCharges' not in df.columns or len(df) < 10:
        raise ValueError("CSV invalido o vacio")
    
except Exception as e:
    print(f"[WARNING] error al cargar csv: {e}")
    print("[INFO] generando datos de prueba...")
    
    # generar datos sinteticos para prueba
    np.random.seed(42)
    n_samples = 5000
    
    df = pd.DataFrame({
        'customerID': [f'ID_{i}' for i in range(n_samples)],
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
    
    # guardar para la proxima ejecucion
    df.to_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv', index=False)
    print("[INFO] datos generados y guardados en data/")

# preprocesamiento
print("[INFO] Preprocesando datos...")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna(subset=['TotalCharges'])

# variables categóricas a encoding
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('customerID')
categorical_cols.remove('Churn')

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# variable objetivo
y = (df['Churn'] == 'Yes').astype(int)
X = df.drop(['customerID', 'Churn'], axis=1)

# dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# escalar los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"[INFO] Dataset split: Train {X_train.shape[0]}, Test {X_test.shape[0]}")
print(f"[INFO] Features: {X.shape[1]}")

# entrenar knn con k=5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)
y_pred_proba_knn = knn.predict_proba(X_test_scaled)[:, 1]

# calcular metricas
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

# guardar el modelo y escalador
print("\n[GUARDANDO] Modelo KNN...")
pickle.dump(knn, open('models/knn.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_knn.pkl', 'wb'))
pickle.dump(label_encoders, open('models/label_encoders.pkl', 'wb'))

# generar graficas de metricas
print("[GENERANDO] Gráficas...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# grafica roc curve
fpr_knn, tpr_knn, _ = roc_curve(y_test, y_pred_proba_knn)
axes[0].plot(fpr_knn, tpr_knn, label=f'KNN (AUC={knn_auc:.3f})', lw=2, color='#10b981')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1)
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve - KNN')
axes[0].legend()
axes[0].grid(alpha=0.3)

# grafica matriz de confusión
sns.heatmap(knn_cm, annot=True, fmt='d', ax=axes[1], cmap='Greens')
axes[1].set_title('Confusion Matrix - KNN')
axes[1].set_ylabel('True Label')
axes[1].set_xlabel('Predicted Label')

plt.tight_layout()
plt.savefig('models/knn_metrics.png', dpi=150, bbox_inches='tight')
print("[OK] Gráficas guardadas en models/knn_metrics.png")

# guardar resumen en archivo txt
with open('models/knn_summary.txt', 'w') as f:
    f.write("=== TELCO CUSTOMER CHURN - K-NEAREST NEIGHBORS ===\n\n")
    f.write(f"Accuracy: {knn_accuracy:.4f}\n")
    f.write(f"Precision: {knn_precision:.4f}\n")
    f.write(f"Recall: {knn_recall:.4f}\n")
    f.write(f"F1-Score: {knn_f1:.4f}\n")
    f.write(f"AUC-ROC: {knn_auc:.4f}\n")
    f.write(f"\nConfusion Matrix:\n{knn_cm}\n")

print("\n[EXITO] Entrenamiento KNN completado!")
