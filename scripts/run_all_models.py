import subprocess
import os

print("=" * 60)
print("ENTRENANDO TODOS LOS MODELOS")
print("=" * 60)

models_to_train = [
    ('Logistic Regression', 'notebooks/train_logistic_regression.py'),
    ('K-Nearest Neighbors', 'notebooks/train_knn.py'),
    ('K-Means Clustering', 'notebooks/train_kmeans.py'),
]

for model_name, script_path in models_to_train:
    print(f"\n[INICIANDO] {model_name}...")
    print("-" * 60)
    
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        print(f"[OK] {model_name} entrenado exitosamente!")
    else:
        print(f"[ERROR] {model_name} falló:")
        print(result.stderr)

print("\n" + "=" * 60)
print("ENTRENAMIENTO COMPLETADO")
print("=" * 60)
print("\nModelos guardados en: models/")
print("  - logistic_regression.pkl")
print("  - knn.pkl")
print("  - kmeans.pkl")
