#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y poppler-utils tesseract-ocr libreoffice ffmpeg

# Install Python dependencies
pip install -r requirements.txt

# Explicitly install MarkItDown with all dependencies
pip install "markitdown[all]"
