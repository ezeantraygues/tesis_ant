import sys
import os
import streamlit as st
import pandas as pd
import sys
import os
# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv(".env.dev")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.common.mongo_manager import MongoManager



#from src.common import mongo_manager
#from src.common.mongo_manager import MongoManager

#from src.common.mongo_manager import MongoManager  # Importar la instancia de MongoManager
#from src.common.mongo_manager import MongoManager



# Streamlit app configuration
st.set_page_config(page_title="Búsqueda Rápida", layout="wide")

def image_carousel(image_list):
    """Displays an image carousel given a list of image URLs or paths."""
    if len(image_list) > 0:
        selected_image = st.slider(
            "Carousel", 0, len(image_list) - 1, 0, format="Image %d"
        )
        st.image(image_list[selected_image], use_container_width=True, caption=f"Image {selected_image + 1}")
    else:
        st.write("No images available to display.")

def search_data(nombre=None, dni=None, patologia=None, texto=None):
    """
    Realiza una búsqueda en la colección de usuarios basada en los parámetros proporcionados.
    Todos los campos son opcionales.
    """
    query = {}

    # Crear consulta insensible a mayúsculas y minúsculas
    if nombre:
        query["paciente"] = {"$regex": f".*{nombre}.*", "$options": "i"}
    if dni:
        query["DNI"] = {"$regex": f".*{dni}.*", "$options": "i"}
    if patologia:
        query["patologia"] = {"$regex": f".*{patologia}.*", "$options": "i"}
    if texto:
        query["$text"] = {"$search": texto}

    # Imprimir la consulta para depuración
    print(f"Consulta generada: {query}")

    # Obtener datos directamente de MongoDB
    mongo_manager = MongoManager()
    data = mongo_manager.get_collection_data("usuarios", query)

    # Convertir los datos obtenidos a DataFrame
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()  # DataFrame vacío si no hay resultados


def main():
    st.title("Búsqueda rápida")

    # Layout for input and search
    col1, col2 = st.columns([1, 3])

    with col1:
        # Text boxes for search inputs
        nombre = st.text_input("Nombre")
        dni = st.text_input("DNI")
        patologia = st.text_input("Patología")
        texto = st.text_input("Búsqueda avanzada")
        
        # Perform search when button is clicked
        if st.button("Search"):
            st.write("Search functionality triggered!")
            # Buscar datos desde la base de datos de MongoDB
            df = search_data(nombre, dni, patologia, texto)
            st.dataframe(df, use_container_width=True)  # Mostrar los resultados en un DataFrame

    with col2:
        # Centered "Resultados" header
        st.markdown("<h3 style='text-align: center;'>Resultados</h3>", unsafe_allow_html=True)

        # Example placeholder for DataFrame
        if 'df' not in locals() or df.empty:
            st.write("No results found for the search.")
        
        # Image carousel placeholder
        st.subheader("Gráficos")
        image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')]
        image_carousel(image_list)


if __name__ == "__main__":
    main()


