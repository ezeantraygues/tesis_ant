# Streamlit code to run the main app

import streamlit as st
from pymongo import MongoClient
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI

# Configurar MongoDB
@st.cache_resource
def connect_to_mongo():
    client = MongoClient("mongodb+srv://<usuario>:<contraseña>@<tu-cluster>.mongodb.net")
    db = client["nombre_de_tu_base_de_datos"]
    return db

# Configurar el LLM
@st.cache_resource
def setup_llm():
    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone(
        "nombre_de_tu_indice",
        embeddings.embed_query,
        "tu_api_key_pinecone",
    )
    retriever = vectorstore.as_retriever()
    llm = AzureChatOpenAI(
        deployment_name="nombre_del_modelo",
        temperature=0.7
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return chain

# Configurar la app
def main():
    st.title("App para tu Proyecto con Streamlit")
    st.sidebar.header("Opciones")
    action = st.sidebar.selectbox("Elige una acción", ["Explorar Base de Datos", "Consultar LLM"])

    db = connect_to_mongo()
    chain = setup_llm()

    if action == "Explorar Base de Datos":
        st.subheader("Explorar Base de Datos")
        collection_name = st.text_input("Nombre de la colección")
        if collection_name:
            collection = db[collection_name]
            documents = list(collection.find().limit(10))  # Muestra 10 documentos
            for doc in documents:
                st.json(doc)

    elif action == "Consultar LLM":
        st.subheader("Consultar al Modelo")
        query = st.text_input("Introduce tu consulta")
        if query:
            response = chain.run(query)
            st.write("**Respuesta del LLM:**")
            st.write(response)

if __name__ == "__main__":
    main()
