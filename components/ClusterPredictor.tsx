"use client"

import type React from "react"
import { useState } from "react"

export default function ClusterPredictor() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    BALANCE: "1500",
    BALANCE_FREQUENCY: "0.5",
    PURCHASES: "500",
    ONEOFF_PURCHASES: "200",
    INSTALLMENTS_PURCHASES: "300",
    CASH_ADVANCE: "100",
    PURCHASES_FREQUENCY: "0.7",
    ONEOFF_PURCHASES_FREQUENCY: "0.3",
    PURCHASES_INSTALLMENTS_FREQUENCY: "0.4",
    CASH_ADVANCE_FREQUENCY: "0.2",
    CASH_ADVANCE_TRX: "2",
    PURCHASES_TRX: "15",
    CREDIT_LIMIT: "5000",
    PAYMENTS: "800",
    MINIMUM_PAYMENTS: "100",
    PRC_FULL_PAYMENT: "0.1",
    TENURE: "12",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const response = await fetch("http://localhost:5000/api/predict-cluster", {
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
      <h2 className="text-xl font-bold text-black mb-4">Segmentación de Clientes (K-Means)</h2>

      {error && <div className="mb-4 p-3 bg-red-100 border border-red-400 rounded text-red-700">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h3 className="font-semibold text-black mb-2">Saldo y Frecuencia</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Saldo ($)</label>
              <input
                type="number"
                name="BALANCE"
                value={formData.BALANCE}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Frecuencia (0-1)</label>
              <input
                type="number"
                name="BALANCE_FREQUENCY"
                value={formData.BALANCE_FREQUENCY}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-black mb-2">Compras</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Compras Totales ($)</label>
              <input
                type="number"
                name="PURCHASES"
                value={formData.PURCHASES}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Una Sola Vez ($)</label>
              <input
                type="number"
                name="ONEOFF_PURCHASES"
                value={formData.ONEOFF_PURCHASES}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">En Cuotas ($)</label>
              <input
                type="number"
                name="INSTALLMENTS_PURCHASES"
                value={formData.INSTALLMENTS_PURCHASES}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Frecuencia (0-1)</label>
              <input
                type="number"
                name="PURCHASES_FREQUENCY"
                value={formData.PURCHASES_FREQUENCY}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-black mb-2">Anticipos y Pagos</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Anticipo ($)</label>
              <input
                type="number"
                name="CASH_ADVANCE"
                value={formData.CASH_ADVANCE}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Pagos ($)</label>
              <input
                type="number"
                name="PAYMENTS"
                value={formData.PAYMENTS}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Pago Mínimo ($)</label>
              <input
                type="number"
                name="MINIMUM_PAYMENTS"
                value={formData.MINIMUM_PAYMENTS}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">% Pago Completo (0-1)</label>
              <input
                type="number"
                name="PRC_FULL_PAYMENT"
                value={formData.PRC_FULL_PAYMENT}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-black mb-2">Crédito y Antigüedad</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-700 mb-1">Límite Crédito ($)</label>
              <input
                type="number"
                name="CREDIT_LIMIT"
                value={formData.CREDIT_LIMIT}
                onChange={handleChange}
                className="w-full px-2 py-1 border border-gray-300 rounded text-black"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-700 mb-1">Antigüedad (meses)</label>
              <input
                type="number"
                name="TENURE"
                value={formData.TENURE}
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
          {loading ? "Prediciendo..." : "Predecir Cluster"}
        </button>
      </form>

      {/* Result */}
      {result && (
        <div className="mt-4 p-4 bg-blue-100 border border-blue-400 rounded">
          <p className="text-blue-800 font-semibold">Cluster: {result.cluster}</p>
          <p className="text-blue-800 text-sm">{result.profile_description}</p>
        </div>
      )}
    </div>
  )
}
