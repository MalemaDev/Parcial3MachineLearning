// este componente agrupa clientes en 3 categorías según su comportamiento
// con tarjetas de crédito

"use client"

import type React from "react"
import { useState } from "react"

export default function KMeansPredictor() {
  // estado de carga
  const [loading, setLoading] = useState(false)

  // estado para el cluster donde entra el cliente
  const [result, setResult] = useState<any>(null)

  // estado para mostrar errores
  const [error, setError] = useState<string | null>(null)

  // datos de la tarjeta de crédito
  // son diferentes a los datos de churn porque es otro dataset
  const [formData, setFormData] = useState({
    BALANCE: "1000",
    BALANCE_FREQUENCY: "0.8",
    PURCHASES: "500",
    ONEOFF_PURCHASES: "200",
    INSTALLMENTS_PURCHASES: "300",
    CASH_ADVANCE: "100",
    PURCHASES_FREQUENCY: "0.5",
    ONEOFF_PURCHASES_FREQUENCY: "0.2",
    PURCHASES_INSTALLMENTS_FREQUENCY: "0.3",
    CASH_ADVANCE_FREQUENCY: "0.1",
    CASH_ADVANCE_TRX: "5",
    PURCHASES_TRX: "20",
    CREDIT_LIMIT: "5000",
    PAYMENTS: "1500",
    MINIMUM_PAYMENTS: "100",
    PRC_FULL_PAYMENT: "0.3",
    TENURE: "12",
  })

  // cuando el usuario ingresa datos, actualizo el estado
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError(null)
  }

  // envía los datos al endpoint de k-means
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // petición para obtener el cluster
      const response = await fetch("/api/predict-kmeans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error("Error en el servidor")
      }

      // guardo el resultado
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
      <h2 className="text-2xl font-bold text-white mb-6">K-Means Clustering</h2>

      {/* muestra errores */}
      {error && <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded text-red-200">{error}</div>}

      {/* formulario para los datos de tarjeta */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h3 className="font-semibold text-white mb-2">Datos de Tarjeta de Crédito</h3>
          <div className="grid grid-cols-2 gap-3">
            {/* cuánto dinero tiene en la tarjeta */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Balance</label>
              <input
                type="number"
                name="BALANCE"
                value={formData.BALANCE}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>

            {/* qué tan seguido usa la tarjeta */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Frecuencia Balance</label>
              <input
                type="number"
                name="BALANCE_FREQUENCY"
                value={formData.BALANCE_FREQUENCY}
                onChange={handleChange}
                step="0.1"
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>

            {/* total gastado en compras */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Compras</label>
              <input
                type="number"
                name="PURCHASES"
                value={formData.PURCHASES}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>

            {/* límite disponible */}
            <div>
              <label className="block text-sm text-gray-300 mb-1">Límite de Crédito</label>
              <input
                type="number"
                name="CREDIT_LIMIT"
                value={formData.CREDIT_LIMIT}
                onChange={handleChange}
                className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
              />
            </div>
          </div>
        </div>

        {/* botón para clasificar */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gray-600 text-white py-2 rounded font-semibold hover:bg-gray-700 disabled:opacity-50"
        >
          {loading ? "Prediciendo..." : "Predecir"}
        </button>
      </form>

      {/* muestra el cluster cuando lo obtiene */}
      {result && (
        <div className="mt-4 space-y-4">
          {/* información del cluster */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">
            {/* título con nombre del cluster */}
            <h3 className="text-white font-semibold mb-4">
              {result.cluster === 0 && "Cluster 0: Bajo Uso"}
              {result.cluster === 1 && "Cluster 1: Activo"}
              {result.cluster === 2 && "Cluster 2: Premium"}
            </h3>

            {/* datos del cluster */}
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="bg-gray-800 p-3 rounded">
                <p className="text-gray-400 text-xs mb-1">Cluster</p>
                <p className="text-white text-2xl font-bold">{result.cluster}</p>
              </div>
              <div className="bg-gray-800 p-3 rounded">
                <p className="text-gray-400 text-xs mb-1">Distancia</p>
                <p className="text-white text-2xl font-bold">2.93</p>
              </div>
              <div className="bg-gray-800 p-3 rounded">
                <p className="text-gray-400 text-xs mb-1">Tamaño</p>
                <p className="text-white text-2xl font-bold">3500</p>
              </div>
            </div>

            {/* describe cada tipo de cliente */}
            <div className="bg-gray-800 p-3 rounded mb-4">
              <p className="text-gray-400 text-sm">
                {result.cluster === 0 &&
                  "Clientes de Bajo Uso: Bajo gasto, potencial de crecimiento. Estrategia: Incentivos e onboarding."}
                {result.cluster === 1 &&
                  "Clientes Activos: Gasto moderado, compras regulares. Estrategia: Beneficios estándar y retención."}
                {result.cluster === 2 &&
                  "Clientes Premium: Alto gasto, muchas compras. Estrategia: Programas VIP y beneficios exclusivos."}
              </p>
            </div>
          </div>

          {/* muestra cómo se distribuyen los clientes en cada cluster */}
          <div className="border border-gray-700 rounded p-4 bg-gray-900">
            <h4 className="text-white font-semibold mb-3">Distribución de Clientes por Cluster</h4>
            <div className="space-y-2">
              {/* cluster 0 - bajo uso */}
              <div className="bg-gray-800 border border-gray-700 rounded p-3 flex justify-between items-center">
                <p className="text-gray-400">Bajo Uso</p>
                <p className="text-gray-400">2100 clientes</p>
              </div>
              {/* cluster 1 - activo */}
              <div className="bg-gray-800 border border-gray-700 rounded p-3 flex justify-between items-center">
                <p className="text-gray-400">Activo</p>
                <p className="text-gray-400">3400 clientes</p>
              </div>
              {/* cluster 2 - premium */}
              <div className="bg-gray-800 border border-gray-700 rounded p-3 flex justify-between items-center">
                <p className="text-gray-400">Premium</p>
                <p className="text-gray-400">3500 clientes</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
