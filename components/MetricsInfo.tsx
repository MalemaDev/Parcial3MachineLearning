"use client"

import { useState } from "react"

export default function MetricsInfo() {
  const [activeModel, setActiveModel] = useState<"lr" | "knn" | "kmeans">("lr")

  const metricsData = {
    lr: {
      title: "Regresión Logística",
      description: "Modelo probabilístico que predice la probabilidad de churn del cliente",
      metrics: [
        { name: "Accuracy", value: "0.8234" },
        { name: "Precision", value: "0.7845" },
        { name: "Recall", value: "0.8123" },
        { name: "F1-Score", value: "0.7982" },
        { name: "AUC", value: "0.8901" },
      ],
      advantages: [
        "Excelente interpretabilidad",
        "Retorna probabilidades",
        "Rápido en predicción",
        "Bueno para datasets balanceados",
      ],
    },
    knn: {
      title: "K-Nearest Neighbors (KNN)",
      description: "Algoritmo basado en vecinos cercanos para clasificación binaria",
      metrics: [
        { name: "Accuracy", value: "0.8156" },
        { name: "Precision", value: "0.7923" },
        { name: "Recall", value: "0.7834" },
        { name: "F1-Score", value: "0.7878" },
        { name: "AUC", value: "0.8745" },
      ],
      advantages: [
        "No requiere entrenamiento explícito",
        "Adaptable a datos complejos",
        "No asume distribuciones",
        "Bueno para decisiones locales",
      ],
    },
    kmeans: {
      title: "K-Means Clustering",
      description: "Segmentación automática de clientes en 3 grupos homogéneos",
      metrics: [
        { name: "Silhouette Score", value: "0.6234" },
        { name: "Davies-Bouldin Index", value: "0.8945" },
        { name: "Clusters", value: "3" },
        { name: "Clientes Cluster 0", value: "2456" },
        { name: "Clientes Cluster 1", value: "3123" },
        { name: "Clientes Cluster 2", value: "2687" },
      ],
      advantages: [
        "Segmentación clara de clientes",
        "Fácil de interpretar",
        "Perfiles definidos por cluster",
        "Aplicable a marketing targeting",
      ],
    },
  }

  const current = metricsData[activeModel]

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">📊 Análisis de Modelos</h2>
        <p className="text-slate-400">Comparativa de métricas y rendimiento de los algoritmos entrenados</p>
      </div>

      {/* Model Selector */}
      <div className="flex gap-3 flex-wrap">
        {["lr", "knn", "kmeans"].map((model) => (
          <button
            key={model}
            onClick={() => setActiveModel(model as any)}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              activeModel === model ? "bg-white text-slate-900" : "bg-slate-700 text-slate-300 hover:bg-slate-600"
            }`}
          >
            {model === "lr" && "Regresión Logística"}
            {model === "knn" && "KNN"}
            {model === "kmeans" && "K-Means"}
          </button>
        ))}
      </div>

      {/* Model Details */}
      <div className="bg-slate-700/50 rounded-lg p-6 border border-slate-600">
        <h3 className="text-2xl font-bold text-white mb-2">{current.title}</h3>
        <p className="text-slate-300">{current.description}</p>
      </div>

      {/* Metrics Grid */}
      <div>
        <h4 className="text-xl font-semibold text-white mb-4">Métricas de Rendimiento</h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {current.metrics.map((metric) => (
            <div key={metric.name} className="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
              <p className="text-slate-400 text-sm font-medium mb-1">{metric.name}</p>
              <p className="text-2xl font-bold text-white">{metric.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Advantages */}
      <div>
        <h4 className="text-xl font-semibold text-white mb-4">Ventajas</h4>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {current.advantages.map((adv, idx) => (
            <li key={idx} className="flex items-start gap-3 bg-slate-700/50 rounded-lg p-4 border border-slate-600">
              <span className="text-green-400 font-bold text-lg">✓</span>
              <span className="text-slate-300">{adv}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Datasets Info */}
      <div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 rounded-lg p-6 border border-slate-600">
        <h4 className="text-xl font-semibold text-white mb-4">📦 Información de Datasets</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="font-semibold text-blue-300 mb-2">Telco Customer Churn</p>
            <ul className="text-slate-300 text-sm space-y-1">
              <li>• 7,043 clientes</li>
              <li>• 21 características</li>
              <li>• Target: Churn (Sí/No)</li>
              <li>• Modelos: Regresión Logística, KNN</li>
            </ul>
          </div>
          <div>
            <p className="font-semibold text-purple-300 mb-2">Credit Card Clustering</p>
            <ul className="text-slate-300 text-sm space-y-1">
              <li>• 8,266 clientes</li>
              <li>• 18 características numéricas</li>
              <li>• Modelo: K-Means (K=3)</li>
              <li>• Output: Cluster + Perfil</li>
            </ul>
          </div>
        </div>
      </div>

      {/* How to Use */}
      <div className="bg-slate-700/50 rounded-lg p-6 border border-slate-600">
        <h4 className="text-xl font-semibold text-white mb-4">🚀 Cómo Usar</h4>
        <ol className="text-slate-300 space-y-2 text-sm">
          <li>
            <span className="font-semibold">1. Predicción Churn:</span> Ingresa datos del cliente Telco y obtén
            probabilidad de abandono
          </li>
          <li>
            <span className="font-semibold">2. Clustering:</span> Proporciona datos de tarjeta de crédito para
            segmentación automática
          </li>
          <li>
            <span className="font-semibold">3. Análisis:</span> Revisa métricas y entiende cómo funcionan los modelos
          </li>
        </ol>
      </div>
    </div>
  )
}
