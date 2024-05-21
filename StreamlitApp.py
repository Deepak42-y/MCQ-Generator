import os
import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
import streamlit as st
from langchain.callbacks import get_openai_callback
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Loading JSON file
try:
    with open("Response.json", 'r') as file:
        RESPONSE_JSON = json.load(file)
except FileNotFoundError:
    st.error("Response.json file not found")
    RESPONSE_JSON = {}

# Create title for the app
st.title("MCQ Generator from given Paragraphs using Langchain 🦜️🔗:")

# Create a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or Text File")

    # Input Fields
    mcq_counts = st.number_input("No. of MCQs to generate:", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject:", max_chars=20)

    # Quiz tone
    tone = st.text_input("Complexity Level of Question:", max_chars=20, placeholder="Simple")

    # Add Button
    button = st.form_submit_button("Create MCQs")

    # Check if Button is clicked and all fields have inputs
    if button and uploaded_file is not None and mcq_counts and subject and tone:
        with st.spinner("Generating..."):
            try:
                # Read the uploaded file
                if uploaded_file.type == "application/pdf":
                    # Reading PDF
                    reader = PyPDF2.PdfFileReader(uploaded_file)
                    text = ""
                    for page in range(reader.numPages):
                        text += reader.getPage(page).extract_text()
                else:
                    # Assuming it is a text file
                    text = uploaded_file.read().decode("utf-8")

                # Count tokens and cost of API
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_counts,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                    # st.write(response)

            except Exception as e:
                logging.error(traceback.format_exc())
                st.error(f"An error occurred: {e}")

            else:
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            # Display review in text box as well
                            st.text_area(label="Review", value=response.get("review", ""))

                        else:
                            st.error("Error in table data")
                else:
                    st.write(response)
