# iris_app/api/app.py

# API Flask para servir un modelo de clasificación de Iris.
from flask import Flask, request, jsonify
import joblib
import json
import os

# Inicializa la app Flask
app = Flask(__name__)

# Ruta del modelo entrenado
modelo_path = "iris_app/model/modelo.pkl"

# Cargar modelo de machine learning al iniciar la API
modelo = joblib.load(modelo_path)

# --- Root endpoint ---
@app.route('/', methods=['GET'])
def index():
    """
    Endpoint raíz que da la bienvenida a la API.
    """
    return jsonify({"message": "Bienvenido a la API del Clasificador de Iris. Visita /health para ver el estado."}), 200

# --- Health endpoint ---
@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de estado de la API.
    
    Método: GET
    Devuelve un mensaje indicando que la API está funcionando
    y el nombre del modelo cargado.
    
    Returns:
        JSON: {"status": "API funcionando", "model": "<nombre_modelo>"}
        HTTP status code: 200
    """
    return jsonify({"status": "API funcionando", "model": "Iris-RandomForest"}), 200

# --- Predict endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para realizar predicciones con el modelo cargado.
    
    Método: POST
    Recibe un JSON con la clave "features" que contiene una lista
    de 4 características para la predicción en el siguiente orden:
    1. Largo del sépalo (cm)
    2. Ancho del sépalo (cm)
    3. Largo del pétalo (cm)
    4. Ancho del pétalo (cm)
    
    Returns:
        JSON: {"prediction": <valor_predicho>}
        HTTP status code: 200 si todo bien, 400 si datos mal estructurados
    """
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Datos mal estructurados"}), 400

    features = data["features"]
    if not isinstance(features, list) or len(features) != 4:
        return jsonify({"error": "La clave 'features' debe ser una lista con 4 elementos."}), 400

    try:
        # El modelo espera una lista de listas (2D array)
        prediction = modelo.predict([features])
        probabilities = modelo.predict_proba([features])
        # Devolvemos el primer elemento de la predicción como un entero
        return jsonify({
            "prediction": int(prediction[0]),
            "probabilities": probabilities[0].tolist() # Convertir a lista para JSON
        }), 200
    except Exception as e:
        # Capturamos cualquier otro error durante la predicción
        return jsonify({"error": f"Error interno al procesar la predicción: {e}"}), 500

# --- Metrics endpoint ---
@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Endpoint para obtener métricas del modelo.
    
    Método: GET
    Lee un archivo JSON con métricas del modelo (precisión, f1-score, etc.)
    y lo devuelve como respuesta.
    
    Returns:
        JSON con métricas si el archivo existe, o un error 404 si no.
    """
    metrics_file = "iris_app/model/metrics.json"
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
        return jsonify(metrics), 200
    else:
        return jsonify({"error": "No se encontraron métricas"}), 404

# Ejecuta la app si se corre directamente este archivo
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
