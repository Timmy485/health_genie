import streamlit as st
import requests
import PyPDF2  # For PDFs
from docx import Document  # For DOCX files
from openai import OpenAI
import os
from os import environ
from dotenv import load_dotenv
load_dotenv()




# st. set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .appview-container .main .block-container {
        padding-top: 2rem;
        margin: 0;
    }
    .css-usj992 {
    background-color: transparent;
    }
    .subtitle {
        margin-bottom: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='text-align: center; padding: 10px;'>SimpliMedi-Assist</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h5 class='subtitle' style='text-align: center; padding: 2px;'>Your Health in Plain English</h5>",
    unsafe_allow_html=True
)


# Create a Streamlit file uploader widget
uploaded_file = st.file_uploader(
    "Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])


# Check if a file has been uploaded
if uploaded_file is not None:
    # Load the document
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "pdf":
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader (uploaded_file)
        text = "".join(
            pdf_reader.pages[page_num]. extract_text()
            for page_num in range(len(pdf_reader.pages))
        )
    elif file_extension == "docx":
        # Extract text from DOCX
        docx_document = Document(uploaded_file)
        text = "".join(paragraph.text + "\n" for paragraph in docx_document.paragraphs)
    elif file_extension == "txt":
        # Read text directly from TXT file
        text = uploaded_file.getvalue().decode("utf-8")

    st.markdown("### Data Preview")
    
    formatted_text = text.replace('\n', '<br>')
    # Create a preview with custom HTML and CSS
    preview_html = """
    <style>
    .preview-container {
        border: 2px solid #007BFF;  # Blue border
        border-radius: 5px; 
        overflow-y: auto; 
        height: 500px; 
        padding: 10px;
    }
    </style>
    <div class="preview-container">""" + formatted_text + "</div>"
        
    st.markdown(preview_html, unsafe_allow_html=True) 


    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key,)

    query = f"""
    Assume you are a patient with limited medical knowledge who has received a medical report filled with complex terminology. You are seeking a clearer understanding of this report in two parts:

    1. **Report Explanation**: First, break down the medical report, keeping the original terms but explaining their significance. Detail what each finding or measurement within the report indicates about your health. Include any abnormalities or conditions detected, explaining what each part of the scan or test represents. 

    2. **Simplified Explanation**: Next, provide a simplified explanation of the report's findings as if explaining to a complete layperson or as though you were explaining it to a two-year-old. This should include:
    - A plain English summary of any conditions or abnormalities found.
    - Insights into how these findings relate to your overall health.
    - Suggestions for potential treatment options or further diagnostic tests, based ONLY on the report's findings.
    - Clarification of any complex terms or concepts in very simple language, avoiding medical jargon.

    Please ensure that while simplifying, you do not omit essential medical terms; rather, introduce them with their explanations to ensure the patient fully understands their report.

    Medical report: {text}
    """


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable agent specializing in the medical domain, proficient in interpreting and analyzing medical reports with precision and expertise.",
            },
            {
                "role": "user", 
                "content": query
            }
        ],
        model="gpt-3.5-turbo",
    )

    st.write(chat_completion.choices[0].message.content)