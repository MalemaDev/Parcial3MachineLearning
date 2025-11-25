# Parcial Final Machine Learning


## Caracteristicas

- Modelos Supervisados (Clasificacion - Dataset Telco)
  - Regresion Logistica: Prediccion probabilistica de Churn
  - K-Nearest Neighbors: Clasificacion KNN de Churn
  - Metricas: ROC, AUC, Matriz de Confusion, Accuracy, Precision, Recall, F1-Score

- Modelo No Supervisado (Clustering - Dataset Credit Card)
  - K-Means: Segmentacion automatica en 3 clusters
  - Analisis: Elbow Method, Silhouette Score, Perfilamiento de clusters

## Instalacion

### 1. Descargar/Clonar el proyecto


git clone <https://github.com/MalemaDev/Parcial3MachineLearning.git>

cd Parcial3MachineLearning


### 2. Instalar dependencias Python


pip install -r requirements.txt

### 3. Entrenar los modelos

Cada modelo se entrena por separado:


# Regresion Logistica
python notebooks/train_logistic_regression.py

# KNN
python notebooks/train_knn.py

# K-Means
python notebooks/train_kmeans.py


Esto generara:
- Modelos en \`models/*.pkl\`
- Graficas en \`models/*.png\`
- Resumen de metricas en \`models/*.txt\`

### 4. Instalar dependencias Frontend


npm install


### 5. Iniciar la aplicacion


npm run dev


Aplicacion disponible en: \`http://localhost:3000\`

## Uso de la Aplicacion

### Pestana 1: Regresion Logistica
1. Llena el formulario con datos del cliente Telco
2. Presiona "Predecir"
3. Obtendras la prediccion de churn y la probabilidad

### Pestana 2: KNN
1. Ingresa los mismos datos
2. Presiona "Predecir"
3. Recibe la clasificacion KNN y los 5 vecinos mas cercanos

### Pestana 3: K-Means
1. Ingresa caracteristicas financieras de tarjeta de credito
2. Presiona "Predecir Cluster"
3. Recibe el numero de cluster y la descripcion del perfil

## Modelos y Metricas

### Regresion Logistica (Telco Churn)
- Accuracy: ~82%
- AUC: ~89%
- Ventajas: Interpretabilidad, probabilidades, rapido

### K-Nearest Neighbors (Telco Churn)
- Accuracy: ~81%
- AUC: ~87%
- Ventajas: No requiere entrenamiento, adaptable, decisiones locales

### K-Means (Credit Card Clustering)
- Silhouette Score: ~0.62
- Clusters: 3 segmentos identificados
- Ventajas: Segmentacion clara, perfiles interpretables, marketing targeting

## Tecnologias

- Backend: Python 3.8+, scikit-learn, pandas, numpy
- Frontend: React 18+, Next.js 16+, TypeScript, Tailwind CSS
- Algoritmos de Machine Learning: Regresion Logistica, KNN, K-Means

## Datasets

### Telco Customer Churn
- Clientes: 7,043
- Caracteristicas: 21
- Target: Churn (Yes/No)
- Modelos: Regresion Logistica, KNN

### Credit Card Clustering
- Clientes: 8,266
- Caracteristicas: 18 numericas
- Modelo: K-Means
- Output: 3 clusters + perfiles

## Troubleshooting

Error: "Modelos no cargados"
- Ejecuta los scripts en \`notebooks/\` para entrenar los modelos

Error: "No se puede conectar a la API"
- Asegura que los modelos esten entrenados
- Verifica los archivos .pkl en la carpeta \`models/\`

---

Desarrollado por Miguel Angel Lema y Jorge Enrique Galvis
