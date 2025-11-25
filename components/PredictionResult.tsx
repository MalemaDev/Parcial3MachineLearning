// componente que muestra el resultado final de las predicciones
// aquí no se predice nada — solo se recibe lo que ya vino del backend
// y se muestra en tarjetas separadas para LR y KNN

"use client"

// interfaz para tipar los datos que vienen desde el backend
// esto evita errores y hace más fácil manejar cada caso (errores, LR, KNN)
interface PredictionData {
  logistic_regression?: {
    prediction: string
    probability_churn: number
    probability_no_churn: number
  }
  knn?: {
    prediction: string
  }
  error?: string
}

// el componente recibe "data" como prop, que contiene lo que el backend respondió
export default function PredictionResult({ data }: { data: PredictionData }) {

  // si el backend mandó error lo mostramos aquí y salimos
  if (data.error) {
    return (
      <div className="mt-8 p-6 bg-red-900 bg-opacity-50 rounded-lg border border-red-600">
        <p className="text-red-400 font-semibold">❌ {data.error}</p>
      </div>
    )
  }

  return (
    <div className="mt-8 space-y-4">

      {/* -------------------------------------- */}
      {/*   SECCIÓN: RESULTADO REGRESIÓN LOGÍSTICA */}
      {/* -------------------------------------- */}
      {data.logistic_regression && (
        <div className="p-6 bg-blue-900 bg-opacity-50 rounded-lg border border-blue-600">

          {/* título de la tarjeta */}
          <h3 className="text-xl font-bold text-white mb-4">📈 Regresión Logística</h3>

          {/* contenido con predicción y probabilidades */}
          <div className="space-y-3">

            {/* predicción principal */}
            <div className="flex justify-between items-center">
              <span className="text-slate-300">Predicción:</span>

              <span
                className={`font-bold text-lg ${
                  data.logistic_regression.prediction === "Sí" ? "text-red-400" : "text-green-400"
                }`}
              >
                {/* si el modelo dice "Sí", es churn */}
                {data.logistic_regression.prediction === "Sí"
                  ? "⚠️ Riesgo de Churn"
                  : "✅ Cliente Fiel"}
              </span>
            </div>

            {/* probabilidad de churn */}
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-300">Probabilidad de Churn:</span>
                <span className="text-yellow-400 font-semibold">
                  {(data.logistic_regression.probability_churn * 100).toFixed(2)}%
                </span>
              </div>

              {/* barra de progreso */}
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div
                  className="bg-yellow-500 h-2 rounded-full"
                  style={{ width: `${data.logistic_regression.probability_churn * 100}%` }}
                ></div>
              </div>
            </div>

            {/* probabilidad de no churn */}
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-300">Probabilidad de Permanencia:</span>
                <span className="text-green-400 font-semibold">
                  {(data.logistic_regression.probability_no_churn * 100).toFixed(2)}%
                </span>
              </div>

              {/* barra de progreso */}
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${data.logistic_regression.probability_no_churn * 100}%` }}
                ></div>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* ---------------------------- */}
      {/*   SECCIÓN: KNN */}
      {/* ---------------------------- */}
      {data.knn && (
        <div className="p-6 bg-indigo-900 bg-opacity-50 rounded-lg border border-indigo-600">

          {/* título */}
          <h3 className="text-xl font-bold text-white mb-4">🎯 K-Nearest Neighbors (KNN)</h3>

          {/* predicción KNN, aquí no hay probabilidades */}
          <div className="flex justify-between items-center">
            <span className="text-slate-300">Predicción:</span>

            <span
              className={`font-bold text-lg ${
                data.knn.prediction === "Sí" ? "text-red-400" : "text-green-400"
              }`}
            >
              {data.knn.prediction === "Sí"
                ? "⚠️ Riesgo de Churn"
                : "✅ Cliente Fiel"}
            </span>
          </div>

        </div>
      )}

    </div>
  )
}
