"""
Configuration and constants for the Markdown Converter UI.
"""

import os
import tempfile
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# File size and cleanup settings
MAX_FILE_SIZE_MB = 50  # Maximum allowed file size in MB
FILE_EXPIRY_HOURS = 2  # Files will be deleted after this many hours

# Temporary directory setup
TEMP_DIR = Path(tempfile.gettempdir()) / "markdown-converter-ui"
TEMP_DIR.mkdir(exist_ok=True, parents=True)

# Dictionary to track temporary files with their creation time
temp_files = {}

# Streamlit configuration
PAGE_TITLE = "Markdown Converter UI"
PAGE_ICON = "📄"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# File types for uploader
ACCEPTED_FILE_TYPES = ["docx", "html", "pdf", "txt", "md", "rtf"]

