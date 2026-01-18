# Resume Analyzer - RAG-based Application

A Streamlit application that analyzes resumes using Groq API and provides intelligent profile matching through RAG (Retrieval-Augmented Generation).

## Features

- **Resume Upload**: Supports PDF and DOCX formats
- **Experience Level Analysis**: Determines if candidate is Entry/Mid/Senior/Expert level
- **Profile Matching**: Uses RAG to match resumes with suitable job profiles
- **Detailed Analysis**: Provides strengths, improvements, and recommendations
- **Profile Database**: Explore different career profiles and their requirements

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get Groq API Key:
   - Visit https://console.groq.com/
   - Create account and get API key

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your Groq API key in the sidebar
2. Upload a resume (PDF or DOCX)
3. View analysis results:
   - Experience level assessment
   - Top 3 matching profiles with similarity scores
   - Detailed analysis with recommendations
   - Explore profile requirements

## Supported Profiles

- Software Engineer
- Data Scientist  
- DevOps Engineer
- Product Manager
- UI/UX Designer

## Technology Stack

- **Streamlit**: Web interface
- **Groq API**: LLM analysis
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **PyPDF2/python-docx**: Document processing