import os
import PyPDF2
import traceback
import json
import streamlit as st
from dotenv import load_dotenv
import base64

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading the PDF file: {str(e)}")
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"Error reading the text file: {str(e)}")
    else:
        raise Exception("Unsupported file format. Only PDF and text files are supported.")
    
import ast




def get_table_data(quiz):
    try:
        # Ensure quiz is not empty
        if not quiz:
            raise ValueError("Empty quiz data received")
        
        # Parse quiz if it's a string
        if isinstance(quiz, str):
            quiz = ast.literal_eval(quiz)
        
        print(f"Quiz: {quiz}")
        
        quiz_table_data = []
        for key, value in quiz.items():
            mcq = value["mcq"]
            options = value["options"]
            correct = value["correct"]
            quiz_table_data.append({
                "Question": mcq,
                "Option A": options.get("a", ""),
                "Option B": options.get("b", ""),
                "Option C": options.get("c", ""),
                "Option D": options.get("d", ""),
                "Correct Answer": correct
            })
            
        return quiz_table_data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")  # Debug statement
        traceback.print_exception(type(e), e, e.__traceback__)
        return []
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return []


def get_table_download_link(df):
    # CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="generated_table.csv">Download as CSV</a>'
    
    # Text
    text = df.to_string(index=False)
    b64 = base64.b64encode(text.encode()).decode()  # B64 encoding
    href += f' | <a href="data:file/txt;base64,{b64}" download="generated_table.txt">Download as Text</a>'
    
    return href