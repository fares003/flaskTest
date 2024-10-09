from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import io

app = Flask(__name__)

def extract_text(input_file):
    input_pdf = PdfReader(input_file)
    total_pages = len(input_pdf.pages)
    
    extracted_text = ""
    for page in range(total_pages):
        extracted_text += input_pdf.pages[page].extract_text()
    
    return extracted_text

@app.route('/extract_text', methods=['POST'])
def extract_text_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        file_stream = io.BytesIO(file.read())
        text = extract_text(file_stream)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
