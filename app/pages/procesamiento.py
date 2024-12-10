import streamlit as st
import pandas as pd
import os

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

def main():
    st.title("Procesamiento")

    # Layout for inputs, results, and buttons
    col1, col2 = st.columns([1, 3])

    with col1:
        # File upload box
        uploaded_file = st.file_uploader("Subir archivo.pdf", type=["pdf"])
        if uploaded_file is not None:
            st.write("File uploaded successfully!")

        # Write results section (placeholder for future implementation)
        st.text_area("Resultados", "Resultados del paciente")
        st.text_area("Conclusiones", "Conclusiones del paciente")
        st.text_area("Recomendaciones", "Recomendaciones del paciente")

    with col2:
        # Centered "Datos extraídos" header
        st.markdown("<h3 style='text-align: center;'>Datos extraídos</h3>", unsafe_allow_html=True)

        # DataFrame visualization
        # Example DataFrame
        data = pd.read_csv('example_data/jhon_doe.csv')
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        # Horizontal buttons below the table
        st.markdown("<hr>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

        with col_btn1:
            if st.button("Edit"):
                st.write("Edit functionality triggered!")  # Placeholder for edit logic

        with col_btn3:
            if st.button("Save"):
                st.write("Save functionality triggered!")  # Placeholder for save logic
        
        with col_btn2:
            if st.button("Cancel"):
                st.write("Cancel functionality triggered!")  # Placeholder for cancel logic

        with col_btn4:
            if st.button("Save & Gen. report"):
                st.write("Save and generate report functionality triggered!")  # Placeholder for report logic

        with col_btn5:
            if st.button("Print"):
                st.write("Print functionality triggered!")  # Placeholder for print logic

        # Image carousel
        st.subheader("Graficos")
        # Example image list (replace with your images)
        image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')]
        image_carousel(image_list)

if __name__ == "__main__":
    main()
