import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pdfminer.high_level import extract_text 

GOOGLE_API_KEY = "AIzaSyBIsM5QX_Qb-V4bLU9zdlTPngeiIMLnp50"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_file.seek(0)  # Ensure the file pointer is at the beginning
        text = extract_text(pdf_file)
        if not text.strip():
            return "Error: No text extracted from PDF"
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


# Function to summarize text using the LLM
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
            # Extract the summary based on the observed structure
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0].get("content", {})
                if "parts" in content and len(content["parts"]) > 0:
                    summary_text = content["parts"][0].get("text", "")
                    if summary_text:
                        return summary_text
                    else:
                        return "Error: No summary text found"
            return "Error: Unable to find summary in the response"

        else:
            return f"Error in LLM processing: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error in LLM processing: {str(e)}"

