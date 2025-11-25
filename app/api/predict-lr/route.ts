// endpoint para regresión logística
// recibe datos del cliente y devuelve si va a hacer churn o no

import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    // obtengo los datos que envió el cliente
    const body = await request.json()

    // aquí normalmente cargaría el modelo entrenado
    // pero para la demo generamos predicciones aleatorias
    // en producción haría: const model = await loadModel(); const prediction = model.predict(body);

    // genero una predicción aleatoria (0 o 1)
    const prediction = Math.random() > 0.5 ? 1 : 0
    // genero una probabilidad aleatoria entre 0 y 1
    const probability = Math.random()

    // devuelvo los resultados en formato json
    return NextResponse.json({
      success: true,
      prediction: prediction === 1 ? "Sí" : "No",
      probability: probability.toFixed(4),
      confidence: Math.abs(probability - 0.5) * 2,
    })
  } catch (error) {
    // si hay error, lo logeo y devuelvo un mensaje de error
    console.error("Error en predicción:", error)
    return NextResponse.json({ success: false, error: "Error al procesar la predicción" }, { status: 500 })
  }
}
