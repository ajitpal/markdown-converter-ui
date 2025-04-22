"""
File handling utilities for the Markdown Converter UI.
"""

import os
import base64
import uuid
import datetime
from pathlib import Path

import streamlit as st

from src.config import TEMP_DIR, MAX_FILE_SIZE_MB, temp_files, logger


def get_download_link(content, filename, text):
    """
    Generate a download link for the content.
    
    Args:
        content (str): The markdown content to be downloaded
        filename (str): The name of the file to be downloaded
        text (str): The text to display for the download link
    
    Returns:
        str: HTML for the download link
    """
    try:
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-button">{text}</a>'
    except Exception as e:
        logger.error(f"Error generating download link: {str(e)}")
        return f'<a href="#" class="download-button error">Error: {str(e)}</a>'


def format_file_size(size_bytes):
    """
    Format file size in a human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
    
    Returns:
        str: Formatted file size (e.g., "5.2 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file (UploadedFile): The uploaded file from Streamlit
    
    Returns:
        str: Path to the saved temporary file
        None: If there was an error saving the file
    """
    try:
        # Check file size
        file_size = len(uploaded_file.getvalue())
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"File exceeds size limit of {MAX_FILE_SIZE_MB}MB. Your file is {file_size / (1024 * 1024):.1f}MB.")
            return None
            
        # Create a unique filename
        unique_id = str(uuid.uuid4())
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_file_name = f"{unique_id}{file_ext}"
        temp_file_path = os.path.join(TEMP_DIR, temp_file_name)
        
        # Save the file
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        # Track the file for cleanup
        temp_files[temp_file_path] = datetime.datetime.now()
        logger.info(f"Created temporary file: {temp_file_path}")
        
        return temp_file_path
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        st.error(f"Error saving file: {str(e)}")
        return None


def validate_file_type(file_name, accepted_types):
    """
    Validate if a file has an accepted file extension.
    
    Args:
        file_name (str): The name of the file
        accepted_types (list): List of accepted file extensions
    
    Returns:
        bool: True if the file type is accepted, False otherwise
    """
    ext = os.path.splitext(file_name)[1].lower().lstrip('.')
    return ext in accepted_types


def get_output_filename(input_filename):
    """
    Generate an output filename for the markdown file.
    
    Args:
        input_filename (str): The name of the input file
    
    Returns:
        str: The name of the output markdown file
    """
    return os.path.splitext(input_filename)[0] + ".md"

