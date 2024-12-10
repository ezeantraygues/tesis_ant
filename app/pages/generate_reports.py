import streamlit as st
import pandas as pd

# Streamlit app configuration
st.set_page_config(page_title="Generate Report", layout="wide")

def main():
    st.title("Generate Report")

    # Layout for inputs, search, and data
    col1, col2 = st.columns([1, 3])

    with col1:
        # Input boxes for patient name and DNI
        patient_name = st.text_input("Nombre")
        if st.button("Search", key="search_name"):
            st.write(f"Search triggered for patient name: {patient_name}")  # Placeholder logic

        patient_dni = st.text_input("DNI")
        if st.button("Search", key="search_dni"):
            st.write(f"Search triggered for patient DNI: {patient_dni}")  # Placeholder logic

    with col2:
        # Header for patient data
        st.markdown("<h3 style='text-align: center;'>Patient Data</h3>", unsafe_allow_html=True)

        # Example DataFrame for patient data
        data = pd.read_csv('example_data/jhon_doe.csv')
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    # Horizontal buttons for Save, Print, and Cancel
    st.markdown("<hr>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("Save report"):
            st.write("Save report functionality triggered!")  # Placeholder for save logic

    with col_btn2:
        if st.button("Print report"):
            st.write("Print report functionality triggered!")  # Placeholder for print logic

    with col_btn3:
        if st.button("Cancel"):
            st.write("Cancel functionality triggered!")  # Placeholder for cancel logic

if __name__ == "__main__":
    main()
