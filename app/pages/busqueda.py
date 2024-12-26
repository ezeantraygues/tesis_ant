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
        query["PACIENTE"] = {"$regex": f".*{nombre}.*", "$options": "i"}
    if dni:
        query["DNI"] = {"$regex": f".*{dni}.*", "$options": "i"}
    if patologia:
        query["PATOLOGIA"] = {"$regex": f".*{patologia}.*", "$options": "i"}
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


# def search_data(nombre, dni, patologia, texto):
#     #"""Searches for documents in MongoDB based on input parameters."""
  
#      query = {}
   

#      if nombre:
#          query["PACIENTE"] = {"$regex": nombre, "$options": "i"} #query["PACIENTE"] = nombre.lower()
#      if dni:
#          query["DNI"] = {"$regex": dni, "$options": "i"}#query["dni"] = dni.lower()
#      if patologia:
#          query["PATOLOGIA"] = {"$regex": patologia, "$options": "i"}#query["patologia"] = patologia.lower()
#      if texto:
#          query["$text"] = {"$search": texto}#query["texto"] = texto.lower()

    

#     # Realizar la consulta en la base de datos usando la clase MongoManager
#     #data = mongo_manager.get_collection_data("usuarios")  # Usar el nombre de la colección que corresponda get_collection_data
#      mongo_manager = MongoManager()
    
#      data = mongo_manager.get_collection_data("usuarios", query)
#      # Verifica si data no está vacío
#    # Si no hay datos, retorna un DataFrame vacío
#      if not data:
#         return pd.DataFrame()

#     # Convierte a DataFrame
#      data = pd.DataFrame(data)

#     # Filtra los datos
#      filtered_data = data[
#         data.apply(lambda row: all(val in str(row.get(col, '')).lower() for col, val in query.items()), axis=1)
#     ]

#      return filtered_data

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


# import os
# import streamlit as st
# import pandas as pd

# # Streamlit app configuration
# st.set_page_config(page_title="Búsqueda Rápida", layout="wide")

# def image_carousel(image_list):
#     """Displays an image carousel given a list of image URLs or paths."""
#     if len(image_list) > 0:
#         selected_image = st.slider(
#             "Carousel", 0, len(image_list) - 1, 0, format="Image %d"
#         )
#         st.image(image_list[selected_image], use_column_width=True, caption=f"Image {selected_image + 1}")
#     else:
#         st.write("No images available to display.")

# def main():
#     st.title("Búsqueda rápida")

#     # Layout for input and search
#     col1, col2 = st.columns([1, 3])

#     with col1:
#         # Text boxes
#         nombre = st.text_input("Nombre")
#         dni = st.text_input("DNI")
#         patologia = st.text_input("Patología")
#         texto = st.text_input("Búsqueda avanzada")
#         if st.button("Search"):
#             st.write("Search functionality triggered!")  # Placeholder for search logic

#     with col2:
#         # Centered "Resultados" header
#         st.markdown("<h3 style='text-align: center;'>Resultados</h3>", unsafe_allow_html=True)

#         # DataFrame visualization
#         # Example DataFrame
#         data = pd.read_csv('example_data/jhon_doe.csv')
#         df = pd.DataFrame(data)
#         st.dataframe(df, use_container_width=True)

#         # Horizontal buttons below the table
#         st.markdown("<hr>", unsafe_allow_html=True)
#         col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns(6)

#         with col_btn1:
#             if st.button("Edit"):
#                 st.write("Edit functionality triggered!")  # Placeholder for edit logic

#         with col_btn3:
#             if st.button("Save"):
#                 st.write("Save functionality triggered!")  # Placeholder for save logic
        
#         with col_btn2:
#             if st.button("Cancel"):
#                 st.write("Cancel functionality triggered!")  # Placeholder for cancel logic

#         with col_btn4:
#             if st.button("Print"):
#                 st.write("Print functionality triggered!")  # Placeholder for print logic

#         with col_btn5:
#             if st.button("Generate report"):
#                 st.write("Generate report functionality triggered!")  # Placeholder for report generation logic


#         # Image carousel placeholder
#         st.subheader("Gráficos")
#         image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')]
#         image_carousel(image_list)


# if __name__ == "__main__":
#     main()


#------------------------------------------------------------------------------------------------------------------------------------------------
# import os
# import streamlit as st
# import pandas as pd
# from src.common.mongo_manager import mongo_manager

# # Streamlit app configuration
# st.set_page_config(page_title="Búsqueda Rápida", layout="wide")

# def image_carousel(image_list):
#     """Displays an image carousel given a list of image URLs or paths."""
#     if len(image_list) > 0:
#         selected_image = st.slider(
#             "Carousel", 0, len(image_list) - 1, 0, format="Image %d"
#         )
#         st.image(image_list[selected_image], use_container_width=True """,use_column_width=True""", caption=f"Image {selected_image + 1}")
#     else:
#         st.write("No images available to display.")


# def main():
#     st.title("Búsqueda en MongoDB")

#     collection_name = st.text_input("Nombre de la colección", "pacientes")
#     query_field = st.text_input("Campo a buscar")
#     query_value = st.text_input("Valor del campo")

#     if st.button("Buscar"):
#         query = {query_field: query_value} if query_field and query_value else {}
#         data = mongo_manager.get_collection_data(collection_name)
        
#         if not data.empty:
#             st.write(data)
#         else:
#             st.warning("No se encontraron datos.")

# if __name__ == "__main__":
#     main()
