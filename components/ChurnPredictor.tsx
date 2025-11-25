"use client"

import type React from "react"
import { useState } from "react"

export default function ChurnPredictor() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [model, setModel] = useState<"logistic" | "knn">("logistic")

  const [formData, setFormData] = useState({
    gender: "Male",
    SeniorCitizen: "0",
    Partner: "Yes",
    Dependents: "No",
    tenure: "12",
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "DSL",
    OnlineSecurity: "No",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: "65",
    TotalCharges: "780",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const endpoint = model === "logistic" ? "/api/predict-churn-lr" : "/api/predict-churn-knn"

      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error("Error en el servidor")
      }

      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
      }
    } catch (err) {
      setError("No se puede conectar con el servidor. Asegúrate que Flask está corriendo.")
      console.error("Error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-black mb-4">Predicción de Churn</h2>

      {error && <div className="mb-4 p-3 bg-red-100 border border-red-400 rounded text-red-700">{error}</div>}

      {/* Model Selection */}
      <div className="mb-4 flex gap-4">
        <label className="flex items-center">
          <input
            type="radio"
            name="model"
            value="logistic"
            checked={model === "logistic"}
            onChange={(e) => setModel(e.target.value as "logistic" | "knn")}
            className="mr-2"
          />
          <span className="text-gray-700">Regresión Logística</span>
        </label>
        <label className="flex items-center">
          <input
            type="radio"
            name="model"
            value="knn"
            checked={model === "knn"}
            onChange={(e) => setModel(e.target.value as "logistic" | "knn")}
            className="mr-2"
          />
          <span className="text-gray-700">K-Nearest Neighbors</span>
        </label>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h3 className="font-semibold text-black mb-2">Información Personal</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Género</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Male</option>
                <option>Female</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">¿Adulto mayor?</label>
              <select
                name="SeniorCitizen"
                value={formData.SeniorCitizen}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option value="0">No</option>
                <option value="1">Sí</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">¿Tiene pareja?</label>
              <select
                name="Partner"
                value={formData.Partner}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Yes</option>
                <option>No</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">¿Dependientes?</label>
              <select
                name="Dependents"
                value={formData.Dependents}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Yes</option>
                <option>No</option>
              </select>
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-black mb-2">Servicios</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Internet</label>
              <select
                name="InternetService"
                value={formData.InternetService}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>DSL</option>
                <option>Fiber optic</option>
                <option>No</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Contrato</label>
              <select
                name="Contract"
                value={formData.Contract}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Month-to-month</option>
                <option>One year</option>
                <option>Two year</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Seguridad</label>
              <select
                name="OnlineSecurity"
                value={formData.OnlineSecurity}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Yes</option>
                <option>No</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Soporte Técnico</label>
              <select
                name="TechSupport"
                value={formData.TechSupport}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              >
                <option>Yes</option>
                <option>No</option>
              </select>
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-black mb-2">Información Financiera</h3>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Antigüedad (meses)</label>
              <input
                type="number"
                name="tenure"
                value={formData.tenure}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Cargos Mensuales</label>
              <input
                type="number"
                name="MonthlyCharges"
                value={formData.MonthlyCharges}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Cargos Totales</label>
              <input
                type="number"
                name="TotalCharges"
                value={formData.TotalCharges}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white py-2 rounded font-semibold hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? "Prediciendo..." : "Predecir"}
        </button>
      </form>

      {/* Result */}
      {result && (
        <div className="mt-4 p-4 bg-green-100 border border-green-400 rounded">
          <p className="text-green-800">
            <strong>Predicción ({model === "logistic" ? "Regresión Logística" : "KNN"}):</strong>
          </p>
          <p className="text-green-800">{result.prediction === 1 ? "✓ Riesgo de Churn" : "✓ Sin riesgo"}</p>
          {result.probability && (
            <p className="text-green-800">Probabilidad: {(result.probability * 100).toFixed(2)}%</p>
          )}
        </div>
      )}
    </div>
  )
}
