"""
Layout management for the Markdown Converter UI.
"""

import streamlit as st

from src.config import ACCEPTED_FILE_TYPES, MAX_FILE_SIZE_MB
from src.ui import components


def sidebar():
    """
    Render the sidebar with info and settings.

    Returns:
        dict: Dictionary containing the user settings
        list: List of uploaded files
    """
    with st.sidebar:
        st.header("About")
        # Display the information
        st.markdown(
            f"""
            This application transforms documents into clean, LLM-ready Markdown for AI workflows.

            ### AI & LLM Integration
            - **Fine-tuning Data Prep**: Prepare training data for LLMs
            - **RAG Systems**: Create content for retrieval-augmented generation
            - **Knowledge Bases**: Build AI-ready documentation
            - **Prompt Engineering**: Extract structured content for prompts

            ### Supported Formats
            - Word Documents (.docx)
            - PDF documents (.pdf)
            - PowerPoint (.pptx)
            - HTML files (.html)
            - Text files (.txt)
            - Markdown files (.md)
            - Rich Text Format (.rtf)
            - Images with OCR (.jpg, .png)
            - Audio transcription (.mp3, .wav)

            ### How to Use
            1. Upload one or more files (max {MAX_FILE_SIZE_MB}MB per file)
            2. Convert to LLM-ready Markdown
            3. Preview the result
            4. Download and use with your AI tools
            """
        )

        st.header("Settings")
        settings = {
            "include_images": st.checkbox(
                "Include images",
                value=True,
                help="When enabled, images from the original document will be embedded in the Markdown."
            ),
            "preserve_tables": st.checkbox(
                "Preserve tables",
                value=True,
                help="When enabled, tables will be preserved as Markdown tables."
            )
        }

        st.markdown("---")
        st.markdown("Built with Streamlit and [MarkItDown](https://github.com/microsoft/markitdown/)")
        st.markdown("*Bridging the gap between documents and AI*")

        return settings


def initialize_session_state():
    """
    Initialize session state variables required for the app.
    """
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = False


def main_content_area():
    """
    Create the main content container.

    Returns:
        container: Streamlit container for the main content
    """
    main_content = st.container()

    with main_content:
        st.subheader("Upload Files")

        # Add file uploader in main content area (the label is already part of the uploader)
        uploaded_files = components.file_uploader()

        if not uploaded_files:
            components.example_section()

    return main_content, uploaded_files


# Clear All functionality has been removed


def render_file_tabs(uploaded_files, _, main_content):
    """
    Render tabs for each uploaded file and manage file processing.

    Args:
        uploaded_files (list): List of uploaded files
        _: Unused parameter (formerly settings, kept for API compatibility)
        main_content: Streamlit container for the main content
    """
    with main_content:
        if uploaded_files:
            st.markdown("---")

            # Mark that files have been processed
            st.session_state.processed_files = True

            # Create tabs for each file
            file_tabs = st.tabs([f.name for f in uploaded_files])

            # Return the tabs and file list
            return file_tabs
        return None


def setup_layout():
    """
    Set up the overall page layout.

    Returns:
        tuple: (settings, uploaded_files, main_content, file_tabs)
    """
    # Initialize session state
    initialize_session_state()

    # Get settings from sidebar
    settings = sidebar()

    # Create main content area with file uploader
    main_content, uploaded_files = main_content_area()

    # Render file tabs if files are uploaded
    file_tabs = render_file_tabs(uploaded_files, settings, main_content)

    return settings, uploaded_files, main_content, file_tabs

