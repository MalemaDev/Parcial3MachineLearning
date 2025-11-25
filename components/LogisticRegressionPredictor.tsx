// componente para predecir si un cliente va a cancelar su suscripción
// usa regresión logística que es un modelo de clasificación

"use client"

import type React from "react"
import { useState } from "react"

export default function LogisticRegressionPredictor() {
  // estado para saber si estamos esperando la respuesta del servidor
  const [loading, setLoading] = useState(false)

  // estado donde guardamos el resultado de la predicción
  const [result, setResult] = useState<any>(null)

  // estado para mostrar mensajes de error si algo falla
  const [error, setError] = useState<string | null>(null)

  // estado con los datos del formulario
  // cada campo es información del cliente que el modelo va a usar para predecir
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

  // cuando el usuario cambia un valor en el formulario, actualizo el estado
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    // limpio errores anteriores
    setError(null)
  }

  // cuando hace click en predecir, mando los datos al servidor
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // hago una petición al endpoint /api/predict-lr
      // envío los datos del cliente en json
      const response = await fetch("/api/predict-lr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error("Error en el servidor")
      }

      // obtengo la respuesta y la guardo en el estado
      const data = await response.json()
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
      }
    } catch (err) {
      // si hay error de conexión, muestro un mensaje
      setError("Error al conectar con el servidor. Intenta de nuevo.")
      console.error("Error:", err)
    } finally {
      // siempre dejo de mostrar la animación de carga
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Regresión Logística</h2>

      {/* muestro error si hay */}
      {error && <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded text-red-200">{error}</div>}

      {/* formulario donde el usuario ingresa los datos */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h3 className="font-semibold text-white mb-2">Información Personal</h3>
          <div className="grid grid-cols-2 gap-3">
            {/* campo de género */}
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

            {/* cuánto tiempo lleva el cliente */}
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

            {/* cuánto paga al mes */}
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

            {/* total pagado hasta ahora */}
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

        {/* botón para hacer la predicción */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gray-600 text-white py-2 rounded font-semibold hover:bg-gray-700 disabled:opacity-50"
        >
          {loading ? "Prediciendo..." : "Predecir"}
        </button>
      </form>

      {/* muestra los resultados cuando llegan del servidor */}
      {result && (
        <div className="mt-6 space-y-4">
          {/* encabezado con checkmark */}
          <div className="flex items-center gap-2 mb-4">
            <span className="text-white text-xl">✓</span>
            <h3 className="text-white font-semibold">Resultado de la Predicción</h3>
          </div>

          {/* la predicción principal */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-gray-400 text-sm mb-1">Predicción</p>
              <p className="text-white text-2xl font-bold">
                {result.prediction === "Sí" ? "CHURN" : "NO CHURN"}
                {result.prediction === "No" && " (Se quedará)"}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-sm mb-1">Confianza</p>
              <p className="text-white text-2xl font-bold">
                {(Number.parseFloat(result.probability) * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          {/* información adicional en cajas */}
          <div className="grid grid-cols-2 gap-2 mb-4">
            <div className="bg-gray-800 p-2 rounded">
              <p className="text-gray-400 text-xs">Antigüedad: {formData.tenure} meses</p>
            </div>
            <div className="bg-gray-800 p-2 rounded">
              <p className="text-gray-400 text-xs">Cargos/Mes: ${formData.MonthlyCharges}</p>
            </div>
            <div className="bg-gray-800 p-2 rounded">
              <p className="text-gray-400 text-xs">Cargos Totales: ${formData.TotalCharges}</p>
            </div>
            <div className="bg-gray-800 p-2 rounded">
              <p className="text-gray-400 text-xs">
                Confianza: {(Number.parseFloat(result.probability) * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          {/* explicación de qué significa el resultado */}
          <div className="bg-gray-800 p-3 rounded">
            <p className="text-gray-400 text-sm">
              {result.prediction === "No"
                ? `Baja probabilidad de churn (${(Number.parseFloat(result.probability) * 100).toFixed(1)}%). Cliente leal. Antigüedad: ${formData.tenure} meses.`
                : `Alta probabilidad de churn (${(Number.parseFloat(result.probability) * 100).toFixed(1)}%). Requiere atención inmediata.`}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
