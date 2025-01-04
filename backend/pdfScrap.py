import PyPDF2
import requests

GOOGLE_API_KEY = "AIzaSyBIsM5QX_Qb-V4bLU9zdlTPngeiIMLnp50"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def summarize_text_with_llm(text):
    try:
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(API_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Parsed Response: {result}")  # Log the parsed response
            
            if result:
                return result
            else:
                return "No summary available. (Response might not match expected structure)"
        else:
            return f"Error in LLM processing: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error in LLM processing: {str(e)}"
