import streamlit as st
import PyPDF2
import docx
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResumeAnalyzer:
    def __init__(self, groq_api_key):
        self.groq_client = Groq(api_key=groq_api_key)
    
    def extract_text_from_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, docx_file):
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_candidate_info(self, resume_text):
        prompt = f"""
        Extract the following information from this resume:
        1. Candidate Name
        2. List of technical skills with proficiency levels (Beginner/Intermediate/Advanced/Expert)
        
        Resume: {resume_text[:2000]}
        
        Format your response as:
        Name: [Candidate Name]
        Skills:
        - [Skill]: [Level]
        - [Skill]: [Level]
        
        If proficiency level is not mentioned, estimate based on experience context.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error extracting info: {str(e)}"

def main():
    st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")
    
    st.title("🎯 Resume Skills Analyzer")
    st.markdown("Upload resume to extract candidate name, skills and skill levels")
    
    # Get API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("❌ GROQ_API_KEY not found in .env file")
        st.info("Please create a .env file with: GROQ_API_KEY=your_api_key")
        return
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer(groq_api_key)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Resume", 
        type=['pdf', 'docx'],
        help="Upload a PDF or DOCX file"
    )
    
    if uploaded_file:
        with st.spinner("Extracting text from resume..."):
            if uploaded_file.type == "application/pdf":
                resume_text = analyzer.extract_text_from_pdf(uploaded_file)
            else:
                resume_text = analyzer.extract_text_from_docx(uploaded_file)
        
        if not resume_text.strip():
            st.error("Could not extract text from the file. Please check the file format.")
            return
        
        # Extract candidate information
        st.subheader("📋 Candidate Information")
        with st.spinner("Extracting candidate details..."):
            candidate_info = analyzer.extract_candidate_info(resume_text)
        
        st.write(candidate_info)

if __name__ == "__main__":
    main()
