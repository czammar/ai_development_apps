"""
Chatbot de recetas
"""

import streamlit as st
import requests

# URL de tu API de FastAPI (asegúrate de que esté corriendo)
API_URL = "http://127.0.0.1:8000"

# --- Funciones de Conexión a la API ---

@st.cache_data
def get_temas():
    """Obtiene la lista de temas disponibles desde la API."""
    try:
        response = requests.get(f"{API_URL}/temas", timeout=60)
        # Lanza un error para códigos de estado HTTP 4xx/5xx
        response.raise_for_status()
        return response.json().get("temas", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de recetas: {e}")
        return []

def get_receta_aleatoria(tema):
    """Obtiene una receta aleatoria para un tema específico."""
    try:
        response = requests.get(f"{API_URL}/receta/{tema}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "nombre": f"Error de Conexión: {e}",
            "tema": tema, "ingredientes": [],
            "pasos": [
                ("No se pudo obtener la receta. Revisa que la API"
                 f"esté corriendo en {API_URL}.")
                 ]
                 }

# --- Interfaz de Usuario y Lógica del Chatbot ---


# Configuración de la página
st.set_page_config(page_title="ChefBot 🤖", layout="wide")
st.title("ChefBot: Tu Generador de Recetas")

# Inicializar el historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Obtener los temas disponibles al inicio
temas_disponibles = get_temas()
temas_str = ", ".join(
    [f"**{t.capitalize()}**" for t in temas_disponibles]
    )

# --- Saludo Inicial del Bot ---
if not st.session_state["messages"]:
    saludo = f"""
    ¡Hola! Soy **ChefBot**, tu asistente virtual de cocina.

    Puedo generar una receta aleatoria para ti. Los temas que puedo
    abordar son: {temas_str}.

    Escribe el **nombre de un tema** (ej: *italiana* o *postres*)
    para comenzar.
    """
    st.session_state["messages"].append(
        {"role": "assistant", "content": saludo}
        )

# Mostrar el historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Lógica de la Entrada del Usuario ---
if prompt := st.chat_input("Escribe el tema de la receta que deseas..."):
    # 1. Agregar el mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Procesar la respuesta del Bot
    with st.chat_message("assistant"):
        tema_solicitado = prompt.strip().lower()

        if tema_solicitado in temas_disponibles:
            # Llamar a la API para obtener la receta
            receta = get_receta_aleatoria(tema_solicitado)

            # Formatear la respuesta de la receta
            receta_respuesta = f"""
            ¡Genial! El Chef recomienda esta receta sobre el tema **{receta['tema'].capitalize()}**:\n
            🥘 {receta['nombre']}\n
            **Ingredientes:**
            {chr(10) + "\n".join(["* " + r for r in receta['ingredientes']])}\n
            **Pasos:**
            {chr(10) + "\n".join(["* " + r for r in receta['pasos']])}\n
            """
            st.markdown(receta_respuesta)
            st.session_state["messages"].append(
                {"role": "assistant", "content": receta_respuesta}
                )

        else:
            # Respuesta si el tema no es válido
            mensaje_error = f"""
            Disculpa, no reconozco el tema **{prompt}**.

            Por favor, elige uno de los temas disponibles: {temas_str}.
            """
            st.markdown(mensaje_error)
            st.session_state["messages"].append({"role": "assistant", "content": mensaje_error})

# Pie de página o información adicional
st.sidebar.header("Temas Disponibles")
if temas_disponibles:
    st.sidebar.info(f"Puedes consultar recetas de:\n- {'\n- '.join(
        t.capitalize() for t in temas_disponibles)}"
        )
else:
    st.sidebar.warning(
        "No se pudo obtener la lista de temas de la API."
        )
