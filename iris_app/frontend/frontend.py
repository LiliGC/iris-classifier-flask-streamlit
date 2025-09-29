# iris_app/frontend/frontend.py

"""
Frontend Streamlit para interactuar con la API Flask que sirve
el modelo de clasificación de Iris. Muestra predicciones, imágenes
y métricas del modelo.
"""

import streamlit as st
import requests
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Configuración de la app
# -----------------------------

# URL de la API (configurable por variable de entorno para Docker)
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

# Inicializar el estado de la sesión para mostrar/ocultar métricas
if 'show_metrics' not in st.session_state:
    st.session_state.show_metrics = False

st.title("🌸 Clasificador de Iris con Flask + Streamlit")
st.markdown("Ajusta los valores de las características de la flor y haz clic en 'Predecir' para ver la clasificación.")

# Información detallada de cada clase (para mostrar después de la predicción)
info_clases = {
    0: {
        "nombre": "Iris Setosa",
        "descripcion": "La Iris Setosa es nativa de Norteamérica y Asia. Se caracteriza por sus pétalos y sépalos más pequeños y redondeados, y es la especie más fácil de distinguir. Sus flores suelen ser de color azul-violeta o blanco.",
        "curiosidad": "Es la especie de Iris más utilizada en estudios botánicos debido a su clara distinción."
    },
    1: {
        "nombre": "Iris Versicolor",
        "descripcion": "La Iris Versicolor, también conocida como 'Blue Flag', es común en humedales de Norteamérica. Sus flores son de tamaño intermedio, con sépalos más anchos y pétalos más estrechos que la Setosa, y a menudo presentan tonos de azul y púrpura.",
        "curiosidad": "Es la flor estatal de Tennessee, aunque a menudo se confunde con la Iris germanica."
    },
    2: {
        "nombre": "Iris Virginica",
        "descripcion": "La Iris Virginica es una especie robusta que se encuentra en el este de Norteamérica. Posee los pétalos y sépalos más grandes y alargados de las tres especies, con flores que varían del azul pálido al púrpura oscuro. Es la más similar a la Versicolor en apariencia.",
        "curiosidad": "Su nombre 'virginica' hace referencia a su prevalencia en el estado de Virginia, EE. UU."
    }
}

# Diccionario de clases y sus nombres
clases = {0: "Setosa 🌱", 1: "Versicolor 🌸", 2: "Virginica 🌺"}

# Obtenemos la ruta absoluta del directorio donde se encuentra este script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas de las imágenes correspondientes a cada clase
imagenes = {
    0: os.path.join(script_dir, "images", "iris_setosa.png"),
    1: os.path.join(script_dir, "images", "iris_versicolor.png"),
    2: os.path.join(script_dir, "images", "iris_virginica.png")
}

# -----------------------------
# Entradas del usuario
# -----------------------------

# Crear dos columnas para el layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Guía Visual")
    diagram_path = os.path.join(script_dir, "images", "iris_diagrama.png")
    st.image(diagram_path, caption="Diferencia entre Sépalo y Pétalo en una flor de Iris.")

with col2:
    st.subheader("Introduce las Medidas")
    with st.form("prediction_form"):
        sepal_length = st.number_input("Largo del sépalo (cm)", min_value=4.0, max_value=8.0, value=5.4, step=0.1)
        sepal_width = st.number_input("Ancho del sépalo (cm)", min_value=2.0, max_value=4.5, value=3.4, step=0.1)
        petal_length = st.number_input("Largo del pétalo (cm)", min_value=1.0, max_value=7.0, value=1.3, step=0.1)
        petal_width = st.number_input("Ancho del pétalo (cm)", min_value=0.1, max_value=2.5, value=0.2, step=0.1)
        
        # Botón de envío dentro del formulario
        submitted = st.form_submit_button("Predecir")

# -----------------------------
# Función de predicción
# -----------------------------
if submitted:
    # Al hacer una nueva predicción, ocultamos las métricas
    st.session_state.show_metrics = False

    # Usar un spinner para dar feedback al usuario mientras espera
    with st.spinner('Realizando la predicción...'):
        try:
            features = [sepal_length, sepal_width, petal_length, petal_width]
            # Añadir un timeout a la petición para evitar esperas infinitas
            response = requests.post(f"{API_URL}/predict", json={"features": features}, timeout=5)

            if response.status_code == 200:
                data = response.json()
                prediction = data["prediction"]
                
                st.success(f"Predicción: **{clases[prediction]}**")
                
                try:
                    img_path = imagenes[prediction]
                    img = Image.open(img_path)
                    st.image(img, caption=f"Ejemplo de {info_clases[prediction]['nombre']}")
                except FileNotFoundError:
                    st.warning(f"Advertencia: No se encontró la imagen para {clases[prediction]}.")

                st.subheader(f"Acerca de {info_clases[prediction]['nombre']}")
                st.write(info_clases[prediction]["descripcion"])
                with st.expander("¿Sabías que...?"):
                    st.write(info_clases[prediction]["curiosidad"])
                st.markdown(f"Más información en [Wikipedia](https://es.wikipedia.org/wiki/Iris_{info_clases[prediction]['nombre'].replace(' ', '_')})")

                if "probabilities" in data:
                    st.subheader("Confianza de la predicción")
                    probabilities = data["probabilities"]
                    
                    # Crear un DataFrame para el gráfico
                    prob_df = pd.DataFrame({
                        "Clase": [clase.split(" ")[0] for clase in clases.values()],
                        "Probabilidad": probabilities
                    })

                    # Crear el gráfico con Matplotlib y Seaborn para mayor control
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.barplot(x="Clase", y="Probabilidad", data=prob_df, ax=ax, palette="viridis", hue="Clase", legend=False)
                    ax.set_ylim(0, 1.1) # Aumentar el límite para que la etiqueta no se corte
                    ax.set_ylabel("Probabilidad")
                    ax.set_xlabel("") # No necesitamos etiqueta en el eje X
                    
                    # Añadir el porcentaje sobre cada barra
                    for index, row in prob_df.iterrows():
                        ax.text(index, row.Probabilidad + 0.02, f"{row.Probabilidad:.1%}", 
                                color='black', ha="center", fontsize=12, weight='bold')

                    st.pyplot(fig)
                    plt.close(fig) # Buena práctica para liberar memoria

            else:
                # Si la API devuelve un error (ej. 400, 500), lo mostramos
                try:
                    error_msg = response.json().get("error", "Error desconocido.")
                    st.error(f"Error desde la API (código {response.status_code}): {error_msg}")
                except requests.exceptions.JSONDecodeError:
                    st.error(f"Error al procesar la respuesta de la API (código {response.status_code}).")

        # Capturar errores de conexión (ej. si la API no está corriendo)
        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexión: No se pudo conectar con la API en {API_URL}. ¿Está el servicio corriendo?")

# -----------------------------
# Mostrar métricas del modelo
# -----------------------------
st.sidebar.header("Información Adicional")

# Sección "Acerca de las Iris" en la barra lateral
st.sidebar.subheader("Acerca de las Iris")
st.sidebar.write(
    "Las Iris son un género de plantas con flor de la familia Iridaceae. "
    "Son conocidas por sus flores vistosas y se utilizan comúnmente en jardinería. "
    "El dataset Iris es uno de los más famosos en Machine Learning."
)
st.sidebar.markdown(
    "Puedes encontrar más información sobre el dataset en el [repositorio de UCI](https://archive.ics.uci.edu/ml/datasets/iris)."
)
st.sidebar.info(
    "El modelo de predicción utilizado es un **Random Forest Classifier** entrenado con Scikit-learn."
)

# Este botón cambia el estado para mostrar u ocultar las métricas
if st.sidebar.button("Ver/Ocultar métricas del modelo"):
    st.session_state.show_metrics = not st.session_state.show_metrics

# Mostramos las métricas solo si el estado es True
if st.session_state.show_metrics:
    with st.spinner("Cargando métricas..."):
        try:
            response = requests.get(f"{API_URL}/metrics", timeout=5)
            
            if response.status_code == 200:
                metrics = response.json()
                
                st.header("Métricas de Rendimiento del Modelo")
                
                st.subheader("Accuracy (Precisión Global)")
                st.metric(label="Accuracy", value=f"{metrics['accuracy']:.2%}")
                
                st.subheader("Reporte de Clasificación")
                st.dataframe(pd.DataFrame(metrics["classification_report"]).transpose())
                
                st.subheader("Matriz de Confusión")
                fig, ax = plt.subplots()
                class_names = ["Setosa", "Versicolor", "Virginica"]
                sns.heatmap(pd.DataFrame(metrics["confusion_matrix"]), annot=True, cmap="Blues", fmt="g", ax=ax)
                ax.set_xlabel("Clase Predicha")
                ax.set_ylabel("Clase Real")
                ax.set_xticklabels(class_names)
                ax.set_yticklabels(class_names)
                st.pyplot(fig)
            else:
                st.error(f"No se pudieron obtener las métricas (código {response.status_code}).")
        except requests.exceptions.RequestException:
            st.error(f"Error de conexión: No se pudo conectar con la API en {API_URL}.")
