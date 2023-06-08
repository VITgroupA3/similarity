import os
from difflib import SequenceMatcher
from PyPDF2 import PdfReader
import streamlit as st

def extract_text_from_pdf(uploaded_pdf):
    pdf = PdfReader(uploaded_pdf)
    text = ''
    for page in range(len(pdf.pages)):
        text += pdf.pages[page].extract_text()
    return text

def compare_texts(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def check_plagiarism(given_pdf, local_pdf_folder):
    given_text = extract_text_from_pdf(given_pdf)
    local_pdfs = os.listdir(local_pdf_folder)

    total_similarity = 0
    for pdf in local_pdfs:
        pdf_path = os.path.join(local_pdf_folder, pdf)
        local_text = extract_text_from_pdf(pdf_path)
        similarity = compare_texts(given_text, local_text)
        st.write(f'{pdf}: {similarity * 100}%')
        total_similarity += similarity

    overall_plagiarism = (total_similarity / len(local_pdfs)) * 100
    st.write(f'\nOverall Plagiarism: {overall_plagiarism}%')

# Streamlit app
st.title('Plagiarism Checker')

# GUI for selecting the given PDF file
given_pdf = st.file_uploader('Select Given PDF File', type='pdf')

# GUI for selecting the local PDF folder
local_pdf_folder = st.text_input('Enter Local PDF Folder Path')

if st.button('Check Plagiarism'):
    if given_pdf is not None and local_pdf_folder:
        check_plagiarism(given_pdf, local_pdf_folder)
    else:
        st.warning('Please select the given PDF file and enter the local PDF folder path.')
