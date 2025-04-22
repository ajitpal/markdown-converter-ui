"""
UI components for the Markdown Converter UI.
"""

import streamlit as st

from src.utils.file_helpers import get_download_link, format_file_size
from src.config import ACCEPTED_FILE_TYPES, MAX_FILE_SIZE_MB


def header():
    """
    Render the application header with logo and description.
    """
    st.markdown(
        """
        <div class="app-header">
            <div class="logo-container">
                <div class="logo-text">
                    <span class="logo-icon">📄</span>Markdown Converter UI
                </div>
                <div class="app-tagline">
                    Professional Document to Markdown Conversion Tool
                </div>
            </div>
            <div class="app-summary">
                <span class="highlight">Bridge the gap between documents and AI</span> — Transform any content into LLM-ready format
            </div>
            <div class="app-description">
                Convert various file formats to clean, well-formatted Markdown using Microsoft's
                <a href="https://github.com/microsoft/markitdown/" target="_blank">MarkItDown</a> library.
                Prepare documents for AI workflows, fine-tuning, and RAG systems with instant conversion of PDFs, Word documents, presentations, and more.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add separator after header
    st.markdown(
        "<hr style='margin: 0 0 20px 0; border: none; height: 1px; background-color: #eaeaea;'>",
        unsafe_allow_html=True
    )


def file_uploader(accepted_types=None):
    """
    Render the file upload component with file type validation.

    Args:
        accepted_types (list, optional): List of accepted file extensions.
            Defaults to the ACCEPTED_FILE_TYPES from config.

    Returns:
        list: List of uploaded files that pass validation
    """
    if accepted_types is None:
        accepted_types = ACCEPTED_FILE_TYPES

    # Create a formatted list of accepted file types for display
    accepted_types_display = ", ".join([f".{ext}" for ext in accepted_types])

    # Add a note about file size limit and accepted types
    uploader_label = f"Choose files to convert (max {MAX_FILE_SIZE_MB}MB per file)"

    # Display accepted file types
    st.caption(f"Accepted file types: {accepted_types_display}")

    # Use Streamlit's file uploader with type restriction
    uploaded_files = st.file_uploader(
        uploader_label,
        accept_multiple_files=True,
        type=accepted_types
    )

    # Additional validation for file types (in case Streamlit's validation is bypassed)
    if uploaded_files:
        valid_files = []
        for file in uploaded_files:
            file_ext = file.name.split('.')[-1].lower() if '.' in file.name else ''
            if file_ext not in accepted_types:
                st.error(f"File '{file.name}' has an unsupported format. Only {accepted_types_display} files are accepted.")
            else:
                valid_files.append(file)
        return valid_files

    return uploaded_files


def file_info(file, file_size=None):
    """
    Display information about a file.

    Args:
        file: The file object
        file_size (int, optional): Size of the file in bytes.
            If None, the size will be computed from the file.
    """
    if file_size is None:
        file_size = len(file.getvalue())

    file_size_formatted = format_file_size(file_size)

    st.markdown(
        f"""
        <div class="file-info">
            <span><strong>File:</strong> {file.name}</span>
            <span><strong>Size:</strong> {file_size_formatted}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def download_button(content, filename, text="Download"):
    """
    Render a download button for the converted markdown.

    Args:
        content (str): The markdown content to be downloaded
        filename (str): The name of the file to be downloaded
        text (str, optional): The text to display on the button. Defaults to "Download".
    """
    st.markdown(
        get_download_link(content, filename, text),
        unsafe_allow_html=True
    )


def success_action_area(content, filename):
    """
    Display a success message with download button.

    Args:
        content (str): The markdown content to be downloaded
        filename (str): The name of the file to be downloaded
    """
    st.markdown(
        f"""
        <div class="action-area">
            <span><strong>✅ Conversion successful!</strong> File is ready to download.</span>
            {get_download_link(content, filename, f"⬇️ Download {filename}")}
        </div>
        """,
        unsafe_allow_html=True
    )


def preview_tabs(markdown_content, filename, tab_index):  # filename is kept for API compatibility
    """
    Create tabs for previewing and viewing raw markdown.

    Args:
        markdown_content (str): The markdown content to display
        filename (str): The name of the output file (not used directly but kept for API compatibility)
        tab_index (int): Index to use for button keys
    """
    # Create the tabs
    preview_tabs = st.tabs(["Preview", "Raw Markdown"])

    # Preview tab
    with preview_tabs[0]:
        # Button row for actions
        col1, _ = st.columns([1, 5])  # Using _ to ignore the second column
        with col1:
            if st.button("Copy Preview", key=f"copy_preview_{tab_index}"):
                st.success("Preview content copied to clipboard!")

        # Display markdown content in a scrollable container
        st.markdown(
            f"<div class='preview-container'>{markdown_content}</div>",
            unsafe_allow_html=True
        )

    # Raw Markdown tab
    with preview_tabs[1]:
        # Button row for actions
        col1, _ = st.columns([1, 5])  # Using _ to ignore the second column
        with col1:
            if st.button("Copy Raw", key=f"copy_raw_{tab_index}"):
                st.success("Raw markdown copied to clipboard!")

        # Display raw markdown in a scrollable container (similar to preview)
        # Escape HTML characters to prevent rendering issues
        escaped_content = markdown_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(
            f"<div class='raw-container'><pre>{escaped_content}</pre></div>",
            unsafe_allow_html=True
        )


def footer():
    """
    Render the application footer.
    """
    # Add a separator before the footer
    st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px; border: none; height: 1px; background-color: #eaeaea;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer">
            <p>Markdown Converter UI - Powered by Microsoft's MarkItDown</p>
            <p>Copyright © 2025</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Clear button functionality has been removed


def example_section():
    """
    Display the example section that shows how the converter works.
    """
    with st.expander("See Example"):
        st.markdown("""
        ### How the Markdown Converter Works

        1. **Upload a Document**: Start by uploading a document (PDF, DOCX, HTML, etc.)

        2. **Automatic Conversion**: The app converts your document to clean Markdown

        3. **Preview Results**: See how your converted document looks

        4. **Download Markdown**: Get the converted Markdown file

        #### Example Input Document (DOCX)

        A Word document with headings, lists, tables, and formatted text.

        #### Example Output (Markdown)

        ```markdown
        # Document Title

        ## Introduction

        This document was automatically converted to **Markdown** format.

        ### Key Features

        - Preserves document structure
        - Maintains formatting like **bold** and *italic* text
        - Converts tables properly

        ## Table Example

        | Name | Description | Value |
        |------|-------------|-------|
        | Item 1 | First item | $10.00 |
        | Item 2 | Second item | $25.00 |

        > Note: The conversion quality depends on the structure of the original document.
        ```

        This app is perfect for:
        - Converting documentation to LLM-ready Markdown
        - Preparing training data for AI fine-tuning workflows
        - Building RAG (Retrieval-Augmented Generation) systems
        - Creating knowledge bases for AI assistants
        - Extracting structured text from PDFs and other documents
        """)

