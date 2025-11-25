// Este componente gestiona las 3 pestañas para cambiar entre los diferentes modelos

"use client"

import { useState } from "react"
import LogisticRegressionPredictor from "@/components/LogisticRegressionPredictor"
import KNNPredictor from "@/components/KNNPredictor"
import KMeansPredictor from "@/components/KMeansPredictor"

export default function Home() {
  // ESTADO: activeTab - controla qué pestaña está visible
  // "lr" = Regresión Logística, "knn" = KNN, "kmeans" = K-Means
  const [activeTab, setActiveTab] = useState<"lr" | "knn" | "kmeans">("lr")

  return (
    <main className="min-h-screen bg-black p-4">
      <div className="max-w-6xl mx-auto">
        {/* TÍTULO */}
        <h1 className="text-3xl font-bold text-white mb-8">Parcial Final Machine Learning</h1>

        {/* PESTAÑAS DE NAVEGACIÓN */}
        <div className="flex gap-4 mb-8 bg-gray-800 p-4 rounded">
          {/* Botón: Regresión Logística */}
          <button
            onClick={() => setActiveTab("lr")}
            className={`px-6 py-2 font-semibold rounded ${
              activeTab === "lr" ? "bg-gray-600 text-white" : "bg-gray-700 text-gray-300"
            }`}
          >
            Regresión Logística
          </button>

          {/* Botón: KNN */}
          <button
            onClick={() => setActiveTab("knn")}
            className={`px-6 py-2 font-semibold rounded ${
              activeTab === "knn" ? "bg-gray-600 text-white" : "bg-gray-700 text-gray-300"
            }`}
          >
            KNN
          </button>

          {/* Botón: K-Means */}
          <button
            onClick={() => setActiveTab("kmeans")}
            className={`px-6 py-2 font-semibold rounded ${
              activeTab === "kmeans" ? "bg-gray-600 text-white" : "bg-gray-700 text-gray-300"
            }`}
          >
            K-Means
          </button>
        </div>

        {/* CONTENIDO DINÁMICO: Muestra el componente según la pestaña activa */}
        <div className="bg-gray-900 p-6 rounded">
          {activeTab === "lr" && <LogisticRegressionPredictor />}
          {activeTab === "knn" && <KNNPredictor />}
          {activeTab === "kmeans" && <KMeansPredictor />}
        </div>
      </div>
    </main>
  )
}
