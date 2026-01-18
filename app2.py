import streamlit as st
import PyPDF2
import docx
from groq import Groq
import os
import pandas as pd
from datetime import datetime
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
        2. Contact Number (phone number)
        3. List of technical skills (comma separated)
        
        Resume: {resume_text[:2000]}
        
        Format your response exactly as:
        Name: [Name]
        Contact: [Phone Number]
        Skills: [Skill1, Skill2, Skill3]
        
        If information is not found, write "Not Found".
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
    
    def parse_info(self, info_text):
        lines = info_text.strip().split('\n')
        name = contact = skills = "Not Found"
        
        for line in lines:
            if line.startswith("Name:"):
                name = line.replace("Name:", "").strip()
            elif line.startswith("Contact:"):
                contact = line.replace("Contact:", "").strip()
            elif line.startswith("Skills:"):
                skills = line.replace("Skills:", "").strip()
        
        return name, contact, skills
    
    def save_to_excel(self, name, contact, skills):
        filename = "resume_data.xlsx"
        
        new_data = {
            'Name': [name],
            'Contact': [contact], 
            'Skills': [skills],
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            new_df = pd.DataFrame(new_data)
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            df = pd.DataFrame(new_data)
        
        df.to_excel(filename, index=False)
        return name, contact, skills

def main():
    st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")
    
    st.title("🎯 Resume Skills Analyzer")
    st.markdown("Upload resume to extract candidate name, contact and skills")
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("❌ GROQ_API_KEY not found in .env file")
        return
    
    analyzer = ResumeAnalyzer(groq_api_key)
    
    uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx'])
    
    if uploaded_file:
        with st.spinner("Processing resume..."):
            if uploaded_file.type == "application/pdf":
                resume_text = analyzer.extract_text_from_pdf(uploaded_file)
            else:
                resume_text = analyzer.extract_text_from_docx(uploaded_file)
        
        if not resume_text.strip():
            st.error("Could not extract text from file.")
            return
        
        with st.spinner("Extracting information..."):
            candidate_info = analyzer.extract_candidate_info(resume_text)
        
        # Parse and save to Excel
        name, contact, skills = analyzer.parse_info(candidate_info)
        analyzer.save_to_excel(name, contact, skills)
        
        # Display data with better formatting
        st.subheader("📊 Candidate Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**👤 Name:**")
            st.info(name)
            
            st.write("**📞 Contact:**")
            st.info(contact)
        
        with col2:
            st.write("**🛠️ Skills:**")
            if skills != "Not Found":
                skill_list = [skill.strip() for skill in skills.split(',')]
                for skill in skill_list:
                    st.write(f"• {skill}")
            else:
                st.info("No skills found")

if __name__ == "__main__":
    main()
