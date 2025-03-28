from flask import Flask, request, jsonify
import tempfile
import subprocess
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    lang = request.form.get('lang', 'ces')  # default: Czech
    file = request.files['file']

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        file.save(pdf_file.name)
        png_path = pdf_file.name.replace(".pdf", "-1.png")

        subprocess.run(["pdftoppm", "-png", "-f", "1", "-l", "1", pdf_file.name, pdf_file.name.replace(".pdf", "")])
        image = Image.open(png_path)
        text = pytesseract.image_to_string(image, lang=lang)

        os.remove(pdf_file.name)
        os.remove(png_path)

        return jsonify({"text": text})

@app.route('/')
def index():
    return "PDF OCR API is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
