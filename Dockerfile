FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-ces poppler-utils && \
    pip install flask pillow pytesseract

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]