import os 
import json
import streamlit as st
import pandas as pd
import traceback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data, get_table_download_link
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")

# Load the response JSON
with open("Response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)

# Create title for the app
st.title("MCQ Generator from given Paragraphs using Langchain 🦜️🔗:")

# Create a form using st.form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or Text File")
    mcq_counts = st.number_input("No. of MCQs to generate:", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject:", max_chars=20)
    tone = st.text_input("Complexity Level of Question:", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_counts and subject and tone:
        with st.spinner("Generating..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_counts,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        print(f"Quiz Data: {quiz}")  # Debug statement to print the quiz data
                        table_data = get_table_data(quiz)
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            # Add download buttons for CSV and text
                            st.markdown("---")
                            st.write("Download generated table")
                            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
                            
                            st.text_area(label="Review", value=response["review"])
                            
                        else:
                            st.error("Error in table data")
                    else:
                        st.error("Quiz data is None")
                else:
                    st.write(response)
