# script para entrenar k-means. este lo usamos para el dataset de tarjetas y para generar los clusters
# tratamos de mantener los pasos claros: cargar datos, preparar, entrenar, evaluar y guardar resultados

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
import pickle
import os

print("[ENTRENANDO] K-Means Clustering...")

# se crean estas carpetas para evitar errores si no existen
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# intento de cargar el csv real. si algo falla, generamos datos sintéticos
try:
    print("[INFO] cargando dataset credit card...")
    df = pd.read_csv('data/CC-GENERAL.csv')
    
    # si el archivo está vacío o raro, lo tomamos como inválido
    if len(df) < 10:
        raise ValueError("csv invalido o vacio")
    
except Exception as e:
    print(f"[WARNING] error al cargar csv: {e}")
    print("[INFO] generando datos de prueba...")
    
    # se generan datos sintéticos por si el archivo original no está
    np.random.seed(42)
    n_samples = 10000
    
    df = pd.DataFrame({
        'CUST_ID': [f'id_{i}' for i in range(n_samples)],
        'BALANCE': np.random.uniform(0, 5000, n_samples),
        'PURCHASES': np.random.uniform(100, 5000, n_samples),
        'CREDIT_LIMIT': np.random.uniform(1000, 30000, n_samples),
        'TENURE': np.random.randint(6, 56, n_samples),
        'NUM_PRODUCTS': np.random.randint(1, 5, n_samples),
        'HAS_CREDIT_CARD': np.random.choice([0, 1], n_samples),
        'IS_ACTIVE_MEMBER': np.random.choice([0, 1], n_samples),
        'CASH_ADVANCE': np.random.uniform(0, 10000, n_samples),
        'REVOLVING_UTILIZATION': np.random.uniform(0, 1, n_samples)
    })
    
    # guardamos el archivo para la próxima vez
    df.to_csv('data/CC-GENERAL.csv', index=False)
    print("[INFO] datos generados guardados en data/")

# preprocesamiento general
print("[INFO] preprocesando datos...")
df = df.dropna()  # quitamos filas nulas para evitar errores en el modelo

# seleccionamos solo columnas numéricas y excluimos el id
X = df.drop('CUST_ID', axis=1)

# escalamos los datos antes de entrenar el modelo
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"[INFO] datos escalados: {X_scaled.shape}")

# análisis para ver cuál k funciona mejor
print("\n[ANALIZANDO] número óptimo de clusters...")
inertias = []
silhouette_scores = []
davies_bouldin_scores = []
K_range = range(2, 11)  # probamos k de 2 a 10

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # guardamos métricas para análisis
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    davies_bouldin_scores.append(davies_bouldin_score(X_scaled, kmeans.labels_))
    
    print(f"k={k}: inertia={kmeans.inertia_:.2f}, silhouette={silhouette_scores[-1]:.4f}")

# entrenamos el modelo final con k=3 (lo dejamos fijo)
print("\n[ENTRENANDO] k-means con k=3...")
kmeans_final = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_final.fit(X_scaled)
labels = kmeans_final.labels_

# impresión de métricas principales
print(f"silhouette score: {silhouette_score(X_scaled, labels):.4f}")
print(f"davies-bouldin index: {davies_bouldin_score(X_scaled, labels):.4f}")
print(f"distribución de clusters: {np.bincount(labels)}")

# perfilamos cada cluster sacando promedios
print("\n[PERFILANDO] clusters...")
df['Cluster'] = labels

cluster_profiles = {}
for cluster in range(3):
    cluster_data = df[df['Cluster'] == cluster]
    profile = cluster_data.drop(['CUST_ID', 'Cluster'], axis=1).mean()
    cluster_profiles[cluster] = profile
    
    # mostramos algunos valores representativos
    print(f"\ncluster {cluster} ({len(cluster_data)} clientes):")
    print(f"  balance promedio: ${profile['BALANCE']:.2f}")
    print(f"  compras promedio: ${profile['PURCHASES']:.2f}")
    print(f"  límite de crédito: ${profile['CREDIT_LIMIT']:.2f}")

# guardamos el modelo, el scaler y los perfiles para usarlos en la app
print("\n[GUARDANDO] modelo k-means...")
pickle.dump(kmeans_final, open('models/kmeans.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_kmeans.pkl', 'wb'))
pickle.dump(cluster_profiles, open('models/cluster_profiles.pkl', 'wb'))

# generamos gráficas del análisis
print("[GENERANDO] gráficas...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# curva elbow
axes[0, 0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('number of clusters (k)')
axes[0, 0].set_ylabel('inertia')
axes[0, 0].set_title('elbow method')
axes[0, 0].grid(alpha=0.3)

# silhouette
axes[0, 1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[0, 1].set_xlabel('number of clusters (k)')
axes[0, 1].set_ylabel('silhouette score')
axes[0, 1].set_title('silhouette analysis')
axes[0, 1].grid(alpha=0.3)

# davies-bouldin
axes[1, 0].plot(K_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
axes[1, 0].set_xlabel('number of clusters (k)')
axes[1, 0].set_ylabel('davies-bouldin index')
axes[1, 0].set_title('davies-bouldin index (lower is better)')
axes[1, 0].grid(alpha=0.3)

# distribución de clusters finales
axes[1, 1].bar(range(3), np.bincount(labels), color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
axes[1, 1].set_xlabel('cluster')
axes[1, 1].set_ylabel('número de clientes')
axes[1, 1].set_title('distribución de clusters (k=3)')
axes[1, 1].set_xticks(range(3))
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('models/kmeans_analysis.png', dpi=150, bbox_inches='tight')
print("[OK] gráficas guardadas en models/kmeans_analysis.png")

# guardar un pequeño resumen en texto
with open('models/kmeans_summary.txt', 'w') as f:
    f.write("=== credit card - k-means clustering ===\n\n")
    f.write("método: k-means con k=3 clusters\n")
    f.write(f"silhouette score: {silhouette_score(X_scaled, labels):.4f}\n")
    f.write(f"davies-bouldin index: {davies_bouldin_score(X_scaled, labels):.4f}\n\n")
    
    descriptions = [
        "cluster 0: clientes de bajo uso",
        "cluster 1: clientes activos",
        "cluster 2: clientes premium"
    ]
    
    for i, desc in enumerate(descriptions):
        f.write(f"{desc}\n")

print("\n[EXITO] entrenamiento k-means completado!")
