# iris_app/model/train_model.py

"""
Entrenamiento de un modelo RandomForest para clasificación de Iris.
Guarda el modelo entrenado en formato joblib (.pkl) para ser usado por la API Flask.
"""

# Importaciones necesarias
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1️⃣ Cargar dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# 2️⃣ Separar datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3️⃣ Entrenar modelo RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4️⃣ Guardar modelo entrenado en archivo .pkl
joblib.dump(model, "iris_app/model/modelo.pkl")
print("✅ Modelo entrenado y guardado en iris_app/model/modelo.pkl")

# 5️⃣ (Opcional) Guardar métricas de evaluación
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y_pred = model.predict(X_test)

# La matriz de confusión necesita ser convertida a lista para ser serializable en JSON
conf_matrix = confusion_matrix(y_test, y_pred).tolist()

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "classification_report": classification_report(y_test, y_pred, output_dict=True),
    "confusion_matrix": conf_matrix
}

import json
with open("iris_app/model/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)
print("✅ Métricas guardadas en iris_app/model/metrics.json")
