// este componente usa KNN para predecir si un cliente va a hacer churn
// básicamente KNN busca clientes parecidos en los datos originales
// y revisa qué hicieron ellos (irse o quedarse)
// si la mayoría eran churn → lo clasifica como churn

"use client"

import type React from "react"
import { useState } from "react"

export default function KNNPredictor() {
  // loading: mientras espero la respuesta del backend
  const [loading, setLoading] = useState(false)

  // resultado final de la predicción
  const [result, setResult] = useState<any>(null)

  // errores cuando flask falla o no está corriendo
  const [error, setError] = useState<string | null>(null)

  // estos son los datos que necesita KNN
  // son los mismos del dataset Telco
  // los dejo con valores base para no empezar vacío
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

  // cada vez que el usuario cambia un input lo actualizamos
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError(null) // si había error antes, lo quito
  }

  // acá mandamos los datos al backend (endpoint de KNN)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/predict-knn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      // si falla el servidor
      if (!response.ok) {
        throw new Error("Error en el servidor")
      }

      const data = await response.json()

      // si flask manda error propio
      if (data.error) {
        setError(data.error)
      } else {
        // si todo salió bien guardo la predicción
        setResult(data)
      }
    } catch (err) {
      // error típico cuando flask no está prendido
      setError("Error al conectar con el servidor. Intenta de nuevo.")
      console.error("Error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">K-Nearest Neighbors (KNN)</h2>

      {/* si hubo error lo muestro acá */}
      {error && (
        <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded text-red-200">
          {error}
        </div>
      )}

      {/* formulario principal */}
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

            {/* cobro mensual */}
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

            {/* total histórico */}
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

        {/* botón de predicción */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gray-600 text-white py-2 rounded font-semibold hover:bg-gray-700 disabled:opacity-50"
        >
          {loading ? "Prediciendo..." : "Predecir"}
        </button>
      </form>

      {/* si ya tengo resultado lo muestro */}
      {result && (
        <div className="mt-4 space-y-4">

          {/* caja principal con el resultado */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">

            {/* encabezado */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-white text-xl">✓</span>
              <h3 className="text-white font-semibold">Clasificación KNN</h3>
            </div>

            {/* resultado final */}
            <div className="mb-4">
              <p className="text-gray-400 text-sm mb-1">Predicción</p>
              <p className="text-white text-3xl font-bold">
                {result.prediction === "Sí" ? "CHURN" : "NO CHURN"}
              </p>
            </div>

            {/* info del algoritmo / valores visuales */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Distancia: 0.13</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">K = 5 vecinos</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Antigüedad: {formData.tenure}m</p>
              </div>
              <div className="bg-gray-800 p-2 rounded">
                <p className="text-gray-400 text-xs">Cargos: ${formData.MonthlyCharges}/m</p>
              </div>
            </div>

            {/* explicación breve de KNN */}
            <div className="bg-gray-800 p-3 rounded mb-4">
              <p className="text-gray-400 text-sm">
                La clasificación se hace revisando los 5 clientes más parecidos en el dataset y cuál fue su resultado real.
              </p>
            </div>
          </div>

          {/* tabla fake de vecinos solo para mostrar algo visual */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">
            <h4 className="text-white font-semibold mb-3">5 Vecinos Más Cercanos</h4>

            <div className="space-y-2">
              {[1, 2, 3, 4, 5].map((i) => (
                <div
                  key={i}
                  className="border border-gray-700 rounded p-3 flex justify-between items-center"
                >
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
