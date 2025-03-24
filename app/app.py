import streamlit as st

st.set_page_config(
    page_title="Procesador de informes",
    page_icon="🏠",
    layout="wide"
)

st.title("Procesador de informes")
st.write("Esta es la página principal de la aplicación.")

# Sidebar for navigation
st.sidebar.title("Navegación")
st.sidebar.page_link("1_procesamiento.py", label="Procesamiento")
st.sidebar.page_link("2_busqueda.py", label="Búsqueda rápida")
st.sidebar.page_link("generate_reports.py", label="Generar Reportes")
st.sidebar.page_link("llm_assistant.py", label="LLM Assistant")

st.write("Selecciona una opción en el menú de la izquierda para comenzar.")

# import streamlit as st

# st.set_page_config(
#     page_title="Form filling App",
#     page_icon="🏠",
#     layout="wide"
# )

# st.title("Welcome to form filling app")
# st.write("This is the main page.")
