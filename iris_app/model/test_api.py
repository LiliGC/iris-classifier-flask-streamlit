# iris_app/model/test_api.py

import requests  # Para hacer solicitudes HTTP a la API

# URL base de la API Flask
BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """
    Prueba el endpoint de salud (/health) de la API Flask.
    
    Envía un GET request al endpoint /health y verifica que el status code sea 200.
    Imprime la respuesta JSON de la API o un mensaje de error en caso de fallo.
    """
    print("🔹 Probando endpoint de salud /health")
    try:
        # Realiza un GET al endpoint de salud
        r = requests.get(BASE_URL + "/health")
        # Lanza excepción si hay un error HTTP
        assert r.status_code == 200, f"Se esperaba 200, pero se obtuvo {r.status_code}"
        
        data = r.json()
        assert data["status"] == "API funcionando"
        print("Respuesta de /health:", data)
        print("✅ OK\n")
    except requests.exceptions.RequestException as e:
        # Muestra error en caso de fallo de conexión o status != 200
        print("❌ Error al conectar con /health:", e)

def test_predict():
    """
    Prueba el endpoint de predicción (/predict) de la API Flask.
    
    Envía POST requests con características de flores Iris en formato JSON.
    Verifica que el status code sea 200 y muestra la predicción devuelta por la API.
    Maneja errores de conexión o respuesta inválida sin interrumpir el script.
    """
    print("🔹 Probando endpoint /predict")

    # Casos de prueba con características de cada clase de Iris
    test_cases = {
        "Setosa_1": {"features": [5.1, 3.5, 1.4, 0.2], "expected": 0},
        "Versicolor_1": {"features": [6.0, 2.2, 4.0, 1.0], "expected": 1},
        "Virginica_1": {"features": [6.2, 3.4, 5.4, 2.3], "expected": 2},
        "Setosa_2": {"features": [4.9, 3.0, 1.4, 0.2], "expected": 0},
        "Versicolor_2": {"features": [5.5, 2.4, 3.7, 1.0], "expected": 1},
        "Virginica_2": {"features": [6.7, 3.0, 5.2, 2.3], "expected": 2}
    }

    # Itera sobre cada caso de prueba
    for label, case in test_cases.items():
        try:
            # Envía POST con las características en formato JSON
            r = requests.post(
                BASE_URL + "/predict",
                json={"features": case["features"]}
            )
            assert r.status_code == 200, f"Se esperaba 200, pero se obtuvo {r.status_code}"
            
            data = r.json()
            prediction = data['prediction']
            assert prediction == case["expected"], f"Para {label}, se esperaba {case['expected']} pero se obtuvo {prediction}"
            
            print(f"✅ {label}: features={case['features']} -> prediction={prediction} (Correcto)")
        except requests.exceptions.RequestException as e:
            # Muestra error en caso de fallo de conexión o status != 200
            print(f"❌ Error al predecir {label}: {e}")

def test_predict_invalid_data():
    """
    Prueba el manejo de errores del endpoint /predict con datos inválidos.
    """
    print("\n🔹 Probando /predict con datos inválidos")

    invalid_cases = {
        "JSON_vacio": ({}, "Datos mal estructurados"),
        "clave_incorrecta": ({"datos": [1,2,3,4]}, "Datos mal estructurados"),
        "features_no_es_lista": ({"features": "no es una lista"}, "La clave 'features' debe ser una lista con 4 elementos."),
        "features_cortas": ({"features": [1, 2, 3]}, "La clave 'features' debe ser una lista con 4 elementos.")
    }

    for label, (payload, expected_error) in invalid_cases.items():
        try:
            r = requests.post(BASE_URL + "/predict", json=payload)
            assert r.status_code == 400
            data = r.json()
            assert data["error"] == expected_error
            print(f"✅ OK: Petición inválida '{label}' manejada correctamente.")
        except Exception as e:
            print(f"❌ Error en prueba de datos inválidos '{label}': {e}")

def test_metrics():
    """
    Prueba el endpoint de métricas (/metrics) de la API Flask.
    
    Verifica que el endpoint devuelva un status 200 y que el JSON
    contenga las claves esperadas.
    """
    print("🔹 Probando endpoint de métricas /metrics")
    try:
        r = requests.get(BASE_URL + "/metrics")
        assert r.status_code == 200, f"Se esperaba 200, pero se obtuvo {r.status_code}"
        
        data = r.json()
        assert "accuracy" in data
        assert "classification_report" in data
        assert "confusion_matrix" in data
        print("✅ OK, métricas recibidas correctamente.\n")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con /metrics: {e}")

# Ejecuta los tests si se corre este archivo directamente
if __name__ == "__main__":
    test_health()   # Probar endpoint de salud
    test_predict()  # Probar endpoint de predicción
    test_predict_invalid_data() # Probar datos inválidos
    test_metrics()  # Probar endpoint de métricas
    print("\n🎉 Todas las pruebas completadas correctamente!")
