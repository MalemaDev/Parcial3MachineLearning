import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
import pickle
import os

print("[ENTRENANDO] K-Means Clustering...")

os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# intentar cargar el csv, si falla generar datos
try:
    print("[INFO] Cargando dataset Credit Card...")
    df = pd.read_csv('data/CC-GENERAL.csv')
    
    # verificar que tenga las columnas correctas
    if len(df) < 10:
        raise ValueError("CSV invalido o vacio")
    
except Exception as e:
    print(f"[WARNING] error al cargar csv: {e}")
    print("[INFO] generando datos de prueba...")
    
    # generar datos sinteticos para prueba
    np.random.seed(42)
    n_samples = 10000
    
    df = pd.DataFrame({
        'CUST_ID': [f'ID_{i}' for i in range(n_samples)],
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
    
    # guardar para la proxima ejecucion
    df.to_csv('data/CC-GENERAL.csv', index=False)
    print("[INFO] datos generados y guardados en data/")

# preprocesamiento
print("[INFO] Preprocesando datos...")
df = df.dropna()

# seleccionar features numéricas (excluyendo ID)
X = df.drop('CUST_ID', axis=1)

# escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"[INFO] Datos escalados: {X_scaled.shape}")

# analizar el número óptimo de clusters con elbow y silhouette
print("\n[ANALIZANDO] Número óptimo de clusters...")
inertias = []
silhouette_scores = []
davies_bouldin_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    davies_bouldin_scores.append(davies_bouldin_score(X_scaled, kmeans.labels_))
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={silhouette_scores[-1]:.4f}")

# entrenar el modelo final con k=3
print("\n[ENTRENANDO] K-Means con K=3...")
kmeans_final = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_final.fit(X_scaled)
labels = kmeans_final.labels_

print(f"Silhouette Score: {silhouette_score(X_scaled, labels):.4f}")
print(f"Davies-Bouldin Index: {davies_bouldin_score(X_scaled, labels):.4f}")
print(f"Distribución de clusters: {np.bincount(labels)}")

# perfilar cada cluster con estadísticas
print("\n[PERFILANDO] Clusters...")
df['Cluster'] = labels

cluster_profiles = {}
for cluster in range(3):
    cluster_data = df[df['Cluster'] == cluster]
    profile = cluster_data.drop(['CUST_ID', 'Cluster'], axis=1).mean()
    cluster_profiles[cluster] = profile
    print(f"\nCluster {cluster} ({len(cluster_data)} clientes):")
    print(f"  Balance promedio: ${profile['BALANCE']:.2f}")
    print(f"  Compras promedio: ${profile['PURCHASES']:.2f}")
    print(f"  Límite de crédito: ${profile['CREDIT_LIMIT']:.2f}")

# guardar modelos y información
print("\n[GUARDANDO] Modelo K-Means...")
pickle.dump(kmeans_final, open('models/kmeans.pkl', 'wb'))
pickle.dump(scaler, open('models/scaler_kmeans.pkl', 'wb'))
pickle.dump(cluster_profiles, open('models/cluster_profiles.pkl', 'wb'))

# generar gráficas del análisis
print("[GENERANDO] Gráficas...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# gráfica elbow curve
axes[0, 0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('Number of Clusters (K)')
axes[0, 0].set_ylabel('Inertia')
axes[0, 0].set_title('Elbow Method')
axes[0, 0].grid(alpha=0.3)

# gráfica silhouette score
axes[0, 1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[0, 1].set_xlabel('Number of Clusters (K)')
axes[0, 1].set_ylabel('Silhouette Score')
axes[0, 1].set_title('Silhouette Analysis')
axes[0, 1].grid(alpha=0.3)

# gráfica davies-bouldin index
axes[1, 0].plot(K_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
axes[1, 0].set_xlabel('Number of Clusters (K)')
axes[1, 0].set_ylabel('Davies-Bouldin Index')
axes[1, 0].set_title('Davies-Bouldin Index (lower is better)')
axes[1, 0].grid(alpha=0.3)

# gráfica distribución de clusters
axes[1, 1].bar(range(3), np.bincount(labels), color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
axes[1, 1].set_xlabel('Cluster')
axes[1, 1].set_ylabel('Número de clientes')
axes[1, 1].set_title('Distribución de Clusters (K=3)')
axes[1, 1].set_xticks(range(3))
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('models/kmeans_analysis.png', dpi=150, bbox_inches='tight')
print("[OK] Gráficas guardadas en models/kmeans_analysis.png")

# guardar descripción de clusters en archivo txt
with open('models/kmeans_summary.txt', 'w') as f:
    f.write("=== CREDIT CARD - K-MEANS CLUSTERING ===\n\n")
    f.write("Método: K-Means con K=3 clusters\n")
    f.write(f"Silhouette Score: {silhouette_score(X_scaled, labels):.4f}\n")
    f.write(f"Davies-Bouldin Index: {davies_bouldin_score(X_scaled, labels):.4f}\n\n")
    
    descriptions = [
        "Cluster 0: Clientes de bajo uso",
        "Cluster 1: Clientes activos",
        "Cluster 2: Clientes premium"
    ]
    
    for i, desc in enumerate(descriptions):
        f.write(f"{desc}\n")

print("\n[EXITO] Entrenamiento K-Means completado!")
