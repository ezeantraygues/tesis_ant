import streamlit as st

# Streamlit app configuration
st.set_page_config(page_title="LLM Assistant (Optional)", layout="wide")

def main():
    st.title("LLM Assistant")

    # Layout for the Results and Conclusions sections
    col1 = st.container()

    with col1:
        # Read-only text area for results
        results = st.text_area(
            "Results",
            "This is where results will be displayed...",
            height=200
            # disabled=True
        )

        # Editable text area for conclusions
        conclusions = st.text_area(
            "Conclusiones",
            height=200
        )

        # Generate conclusions button
        if st.button("Generar conclusiones"):
            st.write("Conclusions generation triggered!")  # Placeholder for LLM integration logic

        # Editable text area for conclusions
        recommendations = st.text_area(
            "recommendations",
            height=200
        )

        # Generate recommendations button
        if st.button("Generar recomendaciones"):
            st.write("recommendations generation triggered!")  # Placeholder for LLM integration logic


    # Horizontal buttons for Cancel and Save
    st.markdown("<hr>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        if st.button("Save"):
            st.write("Save functionality triggered!")  # Placeholder for save logic

    with col_btn2:
        if st.button("Cancel"):
            st.write("Cancel functionality triggered!")  # Placeholder for cancel logic


if __name__ == "__main__":
    main()