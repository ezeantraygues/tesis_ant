import os
import sys
import tempfile
import streamlit as st
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.main_extraction import process_file
from src.generate_sections.main import write_report_from_data

# Configure the page
st.set_page_config(page_title="Procesamiento", layout="wide")

# Cache the file processing to avoid unnecessary reprocessing
@st.cache_data
def process_pdf(file_path):
    return process_file(file_path)

def generate_text(data,results, text_type):
    """Generate new text (resultados, conclusiones, recomendaciones) using AI."""
    return write_report_from_data(data,results, text_type)

def image_carousel(image_list):
    """Displays an image carousel given a list of image paths."""
    if image_list:
        selected_image = st.slider("Carousel", 0, len(image_list) - 1, 0, format="Image %d")
        st.image(image_list[selected_image], use_column_width=True, caption=f"Image {selected_image + 1}")
    else:
        st.write("No images available to display.")

def display_tables(extracted_data):
    """Display the extracted patient and quantitative data in editable tables."""
    st.markdown("<h3 style='text-align: center;'>Datos personales del paciente</h3>", unsafe_allow_html=True)
    df_patient = pd.DataFrame({k: [v] for k, v in extracted_data['patient_data'].items()})
    # Use the data editor so users can modify patient data directly
    edited_patient = st.data_editor(df_patient, use_container_width=True, key="df_patient")
    
    st.markdown("<h3 style='text-align: center;'>Datos cuantitativos del paciente</h3>", unsafe_allow_html=True)
    df_quant = pd.DataFrame({k: [v] for k, v in extracted_data['quantitative_data'].items()})
    # Use the data editor for quantitative data
    edited_quant = st.data_editor(df_quant, use_container_width=True, key="df_quant")
    
    # Optionally, update the extracted_data with edited values
    extracted_data['patient_data'] = edited_patient.to_dict(orient='records')[0]
    extracted_data['quantitative_data'] = edited_quant.to_dict(orient='records')[0]


def main():
    st.title("Procesamiento")
    
    # Initialize session state flags if not set
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    if "processed" not in st.session_state:
        st.session_state.processed = False

    # File upload
    uploaded_file = st.file_uploader("Subir archivo.pdf", type=["pdf"])
    if uploaded_file is not None and not st.session_state.processed:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        with st.spinner("Processing file..."):
            extracted_data = process_pdf(temp_path)
            st.session_state.extracted_data = extracted_data
            st.session_state.processed = True  # Mark file as processed

    if st.session_state.extracted_data:
        extracted_data = st.session_state.extracted_data

        # Display extracted data in two columns
        # col1, col2 = st.columns([1, 3])
        # with col1:
        display_tables(extracted_data)
        # with col2:
        # Display text areas for results, conclusions, and recommendations
        st.subheader("Secciones finales")
        resultados = st.text_area("Resultados", extracted_data['text_fields'].get('resultados', ''))
        conclusiones = st.text_area("Conclusiones", extracted_data['text_fields'].get('conclusiones', ''))
        recomendaciones = st.text_area("Recomendaciones", extracted_data['text_fields'].get('recomendaciones', ''))

        col1, col2, col3 = st.columns(3)
        # Buttons for regenerating text with AI, without triggering pdf reprocessing
        # with col1:
        #     if st.button("Generar Resultados con AI"):
        #         with st.spinner("Generando resultados..."):
        #             nuevos_resultados = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'resultados')
        #             st.session_state.extracted_data['text_fields']['resultados'] = nuevos_resultados
        #             st.experimental_rerun()  # Update UI with new text
        with col2:
            if st.button("Generar Conclusiones con AI"):
                with st.spinner("Generando conclusiones..."): #Check si funciona bien
                    nuevas_conclusiones = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'conclusiones')
                    st.session_state.extracted_data['text_fields']['conclusiones'] = nuevas_conclusiones
                    st.experimental_rerun()
        with col3:
            if st.button("Generar Recomendaciones con AI"):
                with st.spinner("Generando recomendaciones..."): #Check si funciona bien
                    nuevas_recomendaciones = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'recomendaciones')
                    st.session_state.extracted_data['text_fields']['recomendaciones'] = nuevas_recomendaciones
                    st.experimental_rerun()

        # Additional action buttons (e.g., Guardar, Borrar cambios, Descargar)
        st.markdown("<hr>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("Guardar"):
                st.write("Guardando!")  # Implement save logic here
        with col_btn2:
            if st.button("Borrar cambios"):
                st.write("Borrar triggered!")  # Implement cancel/reset logic here
        with col_btn3:
            if st.button("Descargar"):
                st.write("Descargando!")  # Implement download logic here

        # Display image carousel for plots
        st.subheader("Gráficos")
        image_list = extracted_data['plots'][1] #'example_data/plots'
        print(f"plot dir {image_list}")
        # if os.path.exists(plot_dir):
            # image_list = #[os.path.join(plot_dir, plot) for plot in os.listdir(plot_dir)]
        image_carousel(image_list)
        # else:
        #     st.write("No plots directory found.")
    else:
        st.write("No data extracted yet. Please upload a file to see data.")

if __name__ == "__main__":
    main()
