import sys
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env.dev")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.mongo_agent.main import query_mongodb

from src.common.mongo_manager import MongoManager
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
GDRIVE_PLOTS_FOLDER_ID = os.getenv('GDRIVE_PLOTS_FOLDER_ID')
mongo_manager = MongoManager(MONGO_URI, MONGO_DATABASE)

from src.common.pinecone_manager import PineconeManager
pinecone = PineconeManager()

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Búsqueda Rápida", layout="wide")


def image_carousel(image_list):
    """Muestra un carrusel de imágenes a partir de una lista de URLs o rutas."""
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

    #si hay texto, generar 'nombre' para búsqueda exacta. Should be replaced by unique patient id
    if texto:
        results = pinecone.search(texto)
        nombre = [result['paciente'] for result in results]

    if isinstance(nombre, list):
        data = []
        if nombre: 
            for nom in nombre:
                query["paciente"] = {"$regex": f".*{nombre}.*", "$options": "i"}
                data.extend(mongo_manager.get_collection_data(MONGO_COLLECTION, query))
    else:
        # Crear consulta insensible a mayúsculas y minúsculas
        if nombre:
            query["paciente"] = {"$regex": f".*{nombre}.*", "$options": "i"}
        if dni:
            query["DNI"] = {"$regex": f".*{dni}.*", "$options": "i"}
        if patologia:
            query["patologia"] = {"$regex": f".*{patologia}.*", "$options": "i"}
        data = mongo_manager.get_collection_data(MONGO_COLLECTION, query)

    # Convertir los datos obtenidos a DataFrame
    if data:
        for item in data:
            item.pop('plots_paths') #TODO: show plots in UI
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()  # DataFrame vacío si no hay resultados
    
def search_data_mongo(text:str):
    result = query_mongodb(text)
    return pd.DataFrame(result)



def main():
    st.title("Búsqueda")

    # Layout for input and search
    col1, col2 = st.columns([1, 3])

    with col1:
        # Campos de texto para buscar
        st.markdown("<h3 style='text-align: center;'>Búsqueda exacta</h3>", unsafe_allow_html=True)
        nombre = st.text_input("Nombre")
        dni = st.text_input("DNI")
        patologia = st.text_input("Patología")

        st.markdown("<h3 style='text-align: center;'>Búsqueda semántica</h3>", unsafe_allow_html=True)
        texto = st.text_input("Búsqueda semántica")

        # Buscar datos cuando se hace clic en el botón Search
        if st.button("Buscar"):
            # Buscar datos desde la base de datos de MongoDB
            df = search_data(nombre, dni, patologia, texto)
            st.session_state["search_results"] = df
            if not df.empty:
                st.success("Búsqueda completada con éxito.")
            else:
                st.warning("No se encontraron resultados.")

        st.markdown("<h3 style='text-align: center;'>Búsqueda exacta avanzada</h3>", unsafe_allow_html=True)
        texto = st.text_input("Por ej. 'capacidad de amortiguación disminuida'")
        if st.button("Buscar (avanzado)"):
            # Buscar datos desde la base de datos de MongoDB
            df = search_data_mongo(texto)
            print(f"Se encontroe: {df}")
            st.session_state["search_results"] = df
            if not df.empty:
                st.success("Búsqueda completada con éxito.")
            else:
                st.warning("No se encontraron resultados.")
        

    with col2:
        # Mostrar resultados
        st.markdown("<h3 style='text-align: center;'>Resultados</h3>", unsafe_allow_html=True)
        if "search_results" in st.session_state:
            df = st.session_state["search_results"]
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Realiza una búsqueda para ver los resultados.")

        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

        # Editar registro seleccionado
        with col_btn1:
            if "selected_record" not in st.session_state:
                st.session_state["selected_record"] = None

            if st.button("Edit") and "search_results" in st.session_state and not st.session_state["search_results"].empty:
                st.session_state["selected_record"] = st.selectbox(
                    "Seleccione el registro a editar:",
                    st.session_state["search_results"].to_dict(orient="records")
                )
                st.success("Registro seleccionado para editar.")

                # Guardamos el estado original para restaurarlo en caso de "Cancel"
                st.session_state["original_record"] = st.session_state["selected_record"].copy()

            if st.session_state["selected_record"]:
                with st.form("edit_form"):
                    updated_data = {}
                    for column, value in st.session_state["selected_record"].items():
                        if column != "_id":  # Excluir el campo _id
                            updated_data[column] = st.text_input(column, value)

                    submitted = st.form_submit_button("Guardar cambios")
                    if submitted:
                        try:
                            query = {"_id": st.session_state["selected_record"]["_id"]}
                            update = {"$set": updated_data}
                            mongo_manager.update_item("usuarios", query, update)
                            st.success("Datos actualizados con éxito.")
                            # Actualizar los resultados de búsqueda
                            st.session_state["search_results"] = search_data(nombre, dni, patologia, texto)
                        except Exception as e:
                            st.error(f"Error al actualizar los datos: {e}")
        
        with col_btn3:
            if st.button("Cancel") and "original_record" in st.session_state:
                st.session_state["selected_record"] = st.session_state["original_record"].copy()
                st.write("Los cambios han sido cancelados, y los datos han sido restaurados a su estado original.")
                st.session_state["original_record"] = None  # Limpiar el estado original

        with col_btn4:
            if st.button("Descargar"):
                st.write("Descargando!")  # Placeholder for print logic

        # Carrusel de imágenes
        st.subheader("Gráficos")
        image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')] #TODO: get images from gdrive
        image_carousel(image_list)


if __name__ == "__main__":
    main()