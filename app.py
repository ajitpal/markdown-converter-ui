#!/usr/bin/env python3
"""
Markdown Converter UI

A streamlined web interface for converting various file formats to Markdown
using the MarkItDown library from Microsoft.
"""

import sys
import traceback
import os
from pathlib import Path
import streamlit as st

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Markdown Converter UI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Try to import from src module, with fallback handling
try:
    from src.main import main
    from src.utils.cleanup import start_cleanup_thread
except ImportError as e:
    st.error(f"Error importing modules: {str(e)}")
    st.write("Make sure you're running from the correct directory and all dependencies are installed.")
    st.info("Run: pip install -r requirements.txt")
    st.info("Current working directory: " + os.getcwd())
    st.info("Project root: " + str(project_root))
    st.stop()

# Main entry point
if __name__ == "__main__":
    try:
        # Start cleanup thread for temporary files
        cleanup_thread = start_cleanup_thread()
        
        # Run the main application
        main()
    except Exception as e:
        st.error("An unexpected error occurred:")
        st.code(traceback.format_exc())
        st.error(f"Error details: {str(e)}")
        st.info("Please check the troubleshooting section in README.md for common issues and solutions.")
