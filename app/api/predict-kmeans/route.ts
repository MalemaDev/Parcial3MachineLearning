// endpoint para K-Means Clustering
// asigna un cliente a uno de los 3 clusters

import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    // obtengo los datos de la tarjeta
    const body = await request.json()

    // asigno aleatoriamente a un cluster (0, 1 o 2)
    // en producción: calcularía la distancia a cada centroide y elegiría el más cercano
    const cluster = Math.floor(Math.random() * 3)

    // descripción de cada cluster
    const clusterDescriptions = {
      0: "Clientes de bajo uso",
      1: "Clientes activos",
      2: "Clientes premium",
    }

    // devuelvo el cluster asignado y su descripción
    return NextResponse.json({
      success: true,
      cluster: cluster,
      description: clusterDescriptions[cluster as keyof typeof clusterDescriptions],
      profile: {
        balance: Math.random() * 10000,
        purchases: Math.random() * 5000,
        creditLimit: Math.random() * 25000,
      },
    })
  } catch (error) {
    // manejo de errores
    console.error("Error en clustering:", error)
    return NextResponse.json({ success: false, error: "Error al procesar el clustering" }, { status: 500 })
  }
}
