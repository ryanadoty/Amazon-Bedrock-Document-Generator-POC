import streamlit as st
from document_generator import generate_doc, refine_doc


### Title displayed on the Streamlit Web App
st.set_page_config(page_title="Document Generator", page_icon=":tada", layout="wide")


#Header and Subheader dsiplayed in the Web App
with st.container():
    st.header("Press Release Document Generation Assistant")
    st.subheader("")
    st.title("Add details about the Press Release you want to create")

#Setup
with st.container():
    st.write("---")
    st.write("")
    user_input = st.text_area("Press Release Details")


#Saving LLM repsonse as variable
temp_llm_response=""

#Create Buttons and start workflow upon "Submit"
result=st.button("Generate Document")
if result:
    llm_response= generate_doc(user_input)
    st.markdown(llm_response)
    temp_llm_response = llm_response

st.write("---")

    #Create Buttons and start workflow upon "Submit"
user_refine = st.text_area("Add adjustments and recomendations")
result2=st.button("Refine the Document")
if result2:
    llm_refine_response= refine_doc(temp_llm_response, user_refine)
    st.markdown(llm_refine_response)
