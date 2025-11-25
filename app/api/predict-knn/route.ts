// endpoint para K-Nearest Neighbors
// busca los 5 vecinos más cercanos y devuelve la mayoría de clase

import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    // obtengo los datos del cliente
    const body = await request.json()

    // predigo aleatoriamente para la demo
    // en producción: calcularía distancias, buscaría los 5 más cercanos, etc
    const prediction = Math.random() > 0.5 ? 1 : 0
    const probability = Math.random()

    // genero datos simulados de los 5 vecinos más cercanos
    // en real: serían datos actuales del dataset de entrenamiento
    const nearestNeighbors = [
      { index: 1, class: 0 },
      { index: 2, class: 1 },
      { index: 3, class: 0 },
      { index: 4, class: 0 },
      { index: 5, class: 0 },
    ]

    // devuelvo los resultados
    return NextResponse.json({
      success: true,
      prediction: prediction === 1 ? "Sí" : "No",
      probability: probability.toFixed(4),
      confidence: Math.abs(probability - 0.5) * 2,
      nearestNeighbors: nearestNeighbors,
      distance: (Math.random() * 0.5).toFixed(2),
    })
  } catch (error) {
    // manejo de errores
    console.error("Error en predicción KNN:", error)
    return NextResponse.json({ success: false, error: "Error al procesar la predicción" }, { status: 500 })
  }
}
