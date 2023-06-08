import os
from difflib import SequenceMatcher
import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ''
    for page in range(len(pdf.pages)):
        text += pdf.pages[page].extract_text()
    return text

def compare_texts(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def check_plagiarism(given_pdf, local_files):
    given_text = extract_text_from_pdf(given_pdf)

    total_similarity = 0
    total_files = 0
    for file in local_files:
        local_text = extract_text_from_pdf(file)
        similarity = compare_texts(given_text, local_text)
        st.write(f'{file.name}: {similarity * 100}%')
        total_similarity += similarity
        total_files += 1

    overall_plagiarism = (total_similarity / total_files) * 100
    st.write(f'\nOverall Plagiarism: {overall_plagiarism}%')

# Streamlit app
st.title("Plagiarism Checker")

# Upload given PDF file
given_pdf = st.file_uploader("Upload the given PDF file")

# Upload local files
local_files = st.file_uploader("Upload local files", accept_multiple_files=True)

if given_pdf and local_files:
    check_plagiarism(given_pdf, local_files)
