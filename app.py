from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
from streamlit.components.v1 import html

# Add Poppler path
os.environ['PATH'] += os.pathsep + r'C:\Program Files (x86)\poppler-24.07.0\Library\bin'

# Load environment variables
load_dotenv()

genai.configure(api_key="AIzaSyAHd9eGNoaYg9stAjR5faaJv5NX-SDjey4")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>ATS Tracking System</h1>", unsafe_allow_html=True)

input_text = st.text_area("Job Description: ", key="input", height=200)

uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"], help="Limit 200MB per file")

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully", icon="✅")

# Add buttons in columns
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    submit1 = st.button("Tell Me About the Resume")
with col2:
    submit3 = st.button("Percentage Match")
with col3:
    submit4 = st.button("ATS Score Checker")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt4 = """
You are an advanced ATS (Applicant Tracking System) with expertise in analyzing resumes. 
Your task is to score the resume based on how well it aligns with the job description.
Provide a detailed score breakdown highlighting the match with job requirements, keywords used, and overall suitability.
"""

# Add response containers
response_container = st.empty()

if submit1:
    if uploaded_file is not None:
        response_container.markdown("<h3 style='text-align: center;'>Processing...</h3>", unsafe_allow_html=True)
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        response_container.subheader("Evaluation Result")
        response_container.write(response)
    else:
        st.error("Please upload the resume", icon="🚨")

elif submit3:
    if uploaded_file is not None:
        response_container.markdown("<h3 style='text-align: center;'>Processing...</h3>", unsafe_allow_html=True)
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        response_container.subheader("Percentage Match")
        response_container.write(response)
    else:
        st.error("Please upload the resume", icon="🚨")

elif submit4:
    if uploaded_file is not None:
        response_container.markdown("<h3 style='text-align: center;'>Processing...</h3>", unsafe_allow_html=True)
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        response_container.subheader("ATS Score")
        response_container.write(response)
    else:
        st.error("Please upload the resume", icon="🚨")

# Add custom CSS
st.markdown(
    """
    <style>
    .css-1aumxhk { 
        display: none;
    }
    footer {
        visibility: hidden;
    }
    footer:after {
        content: 'Made by Google Gemini';
        visibility: visible;
        display: block;
        position: relative;
        padding: 5px;
        top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
