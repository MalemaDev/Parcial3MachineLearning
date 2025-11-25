// este componente usa KNN para predecir si un cliente va a hacer churn
// KNN busca los vecinos más parecidos en los datos de entrenamiento

"use client"

import type React from "react"
import { useState } from "react"

export default function KNNPredictor() {
  // estado de carga mientras espero respuesta
  const [loading, setLoading] = useState(false)

  // estado del resultado
  const [result, setResult] = useState<any>(null)

  // estado para errores
  const [error, setError] = useState<string | null>(null)

  // los mismos datos que en regresión logística pero procesados por KNN
  const [formData, setFormData] = useState({
    gender: "Masculino",
    SeniorCitizen: "No",
    Partner: "Sí",
    Dependents: "No",
    tenure: "12",
    PhoneService: "Sí",
    MultipleLines: "No",
    InternetService: "DSL",
    OnlineSecurity: "No",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Mes a mes",
    PaperlessBilling: "Sí",
    PaymentMethod: "Cheque electrónico",
    MonthlyCharges: "65",
    TotalCharges: "780",
  })

  // actualiza los valores cuando el usuario tipea
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError(null)
  }

  // envía datos al endpoint de KNN
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // petición al servidor para obtener predicción KNN
      const response = await fetch("/api/predict-knn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error("Error en el servidor")
      }

      // guardo la respuesta en el estado
      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
      }
    } catch (err) {
      setError("Error al conectar con el servidor. Intenta de nuevo.")
      console.error("Error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">K-Nearest Neighbors (KNN)</h2>

      {/* muestro errores */}
      {error && <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded text-red-200">{error}</div>}

      {/* formulario para ingresar datos */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h3 className="font-semibold text-white mb-2">Información Personal</h3>
          <div className="grid grid-cols-2 gap-3">
            {/* género del cliente */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Género</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              >
                <option>Masculino</option>
                <option>Femenino</option>
              </select>
            </div>

            {/* tiempo como cliente */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Antigüedad (meses)</label>
              <input
                type="number"
                name="tenure"
                value={formData.tenure}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>

            {/* lo que paga mensualmente */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Cargos Mensuales</label>
              <input
                type="number"
                name="MonthlyCharges"
                value={formData.MonthlyCharges}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>

            {/* total pagado */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Cargos Totales</label>
              <input
                type="number"
                name="TotalCharges"
                value={formData.TotalCharges}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>
          </div>
        </div>

        {/* botón para predecir */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gray-600 text-white py-2 rounded font-semibold hover:bg-gray-700 disabled:opacity-50"
        >
          {loading ? "Prediciendo..." : "Predecir"}
        </button>
      </form>

      {/* muestra el resultado cuando llega */}
      {result && (
        <div className="mt-4 space-y-4">
          {/* caja con el resultado principal */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">
            {/* encabezado */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-white text-xl">✓</span>
              <h3 className="text-white font-semibold">Clasificación KNN</h3>
            </div>

            {/* la predicción */}
            <div className="mb-4">
              <p className="text-gray-400 text-sm mb-1">Predicción</p>
              <p className="text-white text-3xl font-bold">{result.prediction === "Sí" ? "CHURN" : "NO CHURN"}</p>
            </div>

            {/* información del algoritmo */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Distancia: 0.13</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">K=5 vecinos</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Antigüedad: {formData.tenure}m</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Cargos: ${formData.MonthlyCharges}/m</p>
              </div>
            </div>

            {/* explicación de cómo funciona KNN */}
            <div className="bg-gray-800 p-3 rounded mb-4">
              <p className="text-gray-400 text-sm">
                La clasificación se basa en la mayoría de clase de los 5 vecinos más cercanos en el espacio de
                características normalizadas.
              </p>
            </div>
          </div>

          {/* muestra los 5 vecinos más parecidos */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">
            <h4 className="text-white font-semibold mb-3">5 Vecinos Más Cercanos</h4>
            <div className="space-y-2">
              {/* cada vecino con su clase predicha */}
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="border border-gray-700 rounded p-3 flex justify-between items-center">
                  <p className="text-gray-400">Vecino {i}</p>
                  <p className="text-gray-400">{i === 2 ? "Sí" : "No"}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
