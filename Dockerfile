FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Explicitly install MarkItDown with all dependencies
RUN pip install "markitdown[all]"

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
