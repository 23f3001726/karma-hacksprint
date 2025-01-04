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
        # Prepare request payload
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

        # Set headers
        headers = {
            "Content-Type": "application/json"
        }

        # Send the request to the Gemini LLM API
        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            print(result)  # Log the response to understand its structure
            return result 
            # Extract the summarized text from the response
            # return result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "No summary available.")
        else:
            return f"Error in LLM processing: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error in LLM processing: {str(e)}"
