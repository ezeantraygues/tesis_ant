import tempfile
import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from dotenv import load_dotenv
load_dotenv(".env.dev")
from src.main_extraction import process_file
from src.generate_sections.main import write_report_from_data

# Streamlit app configuration
st.set_page_config(page_title="Procesamiento", layout="wide")

def image_carousel(image_list):
    """Displays an image carousel given a list of image URLs or paths."""
    if len(image_list) > 0:
        selected_image = st.slider(
            "Carousel", 0, len(image_list) - 1, 0, format="Image %d"
        )
        st.image(image_list[selected_image], use_column_width=True, caption=f"Image {selected_image + 1}")
    else:
        st.write("No images available to display.")

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {}


def main():
    st.title("Procesamiento")

    extracted_data = st.session_state.extracted_data


    # Layout for inputs, results, and buttons
    col1, col2 = st.columns([1, 3])

    with col1:
        # File upload box
        uploaded_file = st.file_uploader("Subir archivo.pdf", type=["pdf"])
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            # extracted_data = process_file(uploaded_file)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())  # Save uploaded file to temp location
                temp_path = tmp_file.name

            with st.spinner("Processing file..."):
                print(temp_path)
                extracted_data = process_file(temp_path)
                st.session_state.processed = True  # Prevent reprocessing
                # extracted_data = st.session_state.extracted_data
            print(extracted_data)

    with col2:
        if extracted_data:
            # Centered "Datos extraídos" header
            st.markdown("<h3 style='text-align: center;'>Datos personales del paciente</h3>", unsafe_allow_html=True)
            patient_data = {k:[v] for k,v in extracted_data['patient_data'].items()}
            df = pd.DataFrame(patient_data)
            st.dataframe(df, use_container_width=True) #TODO: Should be editable!

            # Centered "Datos extraídos" header
            st.markdown("<h3 style='text-align: center;'>Datos cuantitativos del paciente</h3>", unsafe_allow_html=True)
            quantitative_data = {k:[v] for k,v in extracted_data['quantitative_data'].items()}
            df = pd.DataFrame(quantitative_data)
            st.dataframe(df, use_container_width=True) #TODO: Should be editable!

            st.text_area("Resultados", extracted_data['text_fields'].get('resultados', ''), key="resultados")
            if st.button("Generar Resultados con AI"):
                st.write("Generando!")  # Placeholder for save logic
                resultados = write_report_from_data(extracted_data['quantitative_data'],'resultados')
                st.text_area("Resultados", resultados, key="resultados") #TODO: fixear como se sobreescribe acá

            st.text_area("Conclusiones", extracted_data['text_fields'].get('conclusiones', ''))
            if st.button("Generar Conclusiones con AI"):
                st.write("Generando!")  # Placeholder for save logic
                conclusiones = write_report_from_data(extracted_data['quantitative_data'],'conclusiones')
            st.text_area("Recomendaciones", extracted_data['text_fields'].get('recomendaciones', ''))
            if st.button("Generar Recomendaciones con AI"):
                st.write("Generando!")  # Placeholder for save logic
                recomendaciones = write_report_from_data(extracted_data['quantitative_data'],'recomendaciones')

            # Horizontal buttons below the table
            st.markdown("<hr>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3= st.columns(3)

            with col_btn1:
                if st.button("Guardar"):
                    st.write("Guardando!")  # Placeholder for save logic
            
            with col_btn2:
                if st.button("Borrar cambios"):
                    st.write("Borrar triggered!")  # Placeholder for cancel logic

            with col_btn3:
                if st.button("Descargar"):
                    st.write("Descargando!")  # Placeholder for print logic

        else:
            st.write("No data extracted yet. Please upload a file to see data.")

        

        # Image carousel
        if extracted_data:
            st.subheader("Graficos")
            image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')]
            # image_list = [extracted_data['plots'][1]] #TODO: fix this
            image_carousel(image_list)
        else:
            st.write("No data extracted yet. Please upload a file to see plots.")

if __name__ == "__main__":
    main()
