"""
Markdown conversion utilities for the Markdown Converter UI.
"""

import os
import streamlit as st
from markitdown import MarkItDown, FileConversionException, DocumentConverterResult

from src.config import MAX_FILE_SIZE_MB, logger


def convert_to_markdown(file_path, options=None, status_placeholder=None, progress_bar=None):
    """
    Convert a file to markdown using the MarkItDown library.

    Args:
        file_path (str): Path to the file to convert
        options (dict, optional): Conversion options. Defaults to None.
        status_placeholder (st.empty, optional): Status placeholder for updates. Defaults to None.
        progress_bar (st.progress, optional): Progress bar for visual feedback. Defaults to None.

    Returns:
        str: The converted markdown content
        None: If conversion failed
    """
    try:
        # Create converter with built-ins explicitly enabled
        converter = MarkItDown(enable_builtins=True)

        if status_placeholder:
            status_placeholder.text("Analyzing file...")
        if progress_bar:
            progress_bar.progress(20)

        # Use convert_local for local files with proper options
        conversion_kwargs = options if options else {}

        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        logger.info(f"Processing file: {file_path} ({file_size_mb:.1f}MB)")

        if file_size_mb > MAX_FILE_SIZE_MB:
            error_msg = f"File exceeds size limit of {MAX_FILE_SIZE_MB}MB. Your file is {file_size_mb:.1f}MB."
            if status_placeholder:
                status_placeholder.error(error_msg)
            logger.warning(f"File size limit exceeded: {file_path} ({file_size_mb:.1f}MB)")
            return None
        elif file_size_mb > MAX_FILE_SIZE_MB * 0.7:  # Warn if file is approaching limit
            warning_msg = f"Large file detected ({file_size_mb:.1f}MB). Processing may take longer."
            if status_placeholder:
                status_placeholder.warning(warning_msg)
            logger.info(warning_msg)

        # Update status
        if status_placeholder:
            status_placeholder.text("Converting file to Markdown...")
        if progress_bar:
            progress_bar.progress(40)

        # Process file
        try:
            result = converter.convert_local(path=file_path, **conversion_kwargs)
            if progress_bar:
                progress_bar.progress(80)
        except Exception as e:
            if status_placeholder:
                status_placeholder.error(f"Error converting file: {str(e)}")
            logger.error(f"Error in file conversion: {str(e)}")
            return None

        # Get markdown content from result
        markdown_content = None
        if isinstance(result, DocumentConverterResult):
            markdown_content = result.markdown
        elif hasattr(result, 'markdown'):
            markdown_content = result.markdown
        elif hasattr(result, 'get_markdown'):
            markdown_content = result.get_markdown()
        elif isinstance(result, str):
            markdown_content = result
        else:
            if status_placeholder:
                status_placeholder.warning(f"Unexpected result type: {type(result)}")
            markdown_content = str(result)

        if progress_bar:
            progress_bar.progress(100)
        if status_placeholder:
            status_placeholder.text("Conversion complete!")

        return markdown_content
    except FileConversionException as e:
        if status_placeholder:
            status_placeholder.error(f"Conversion failed: {str(e)}")
        logger.error(f"FileConversionException: {str(e)}")
        return None
    except Exception as e:
        if status_placeholder:
            status_placeholder.error(f"Unexpected error: {str(e)}")
        logger.exception("Exception during file conversion")
        return None


def render_markdown(markdown_text):
    """
    Safely render markdown content with proper formatting.

    Args:
        markdown_text (str): The markdown text to render

    Returns:
        bool: True if rendering was successful, False otherwise
    """
    try:
        # Create a container to hold all markdown content
        with st.container():
            # Process code blocks separately to ensure proper syntax highlighting
            lines = markdown_text.split('\n')
            in_code_block = False
            code_block_content = []
            language = ""
            current_text = []

            for line in lines:
                if line.startswith('```'):
                    if in_code_block:  # End of code block
                        # Render accumulated text before code block
                        if current_text:
                            st.markdown('\n'.join(current_text))
                            current_text = []

                        # Render code block with syntax highlighting
                        st.code('\n'.join(code_block_content), language=language)
                        code_block_content = []
                        language = ""
                        in_code_block = False
                    else:  # Start of code block
                        # Render accumulated text
                        if current_text:
                            st.markdown('\n'.join(current_text))
                            current_text = []

                        # Extract language if specified
                        language = line[3:].strip() if len(line) > 3 else ""
                        in_code_block = True
                elif in_code_block:
                    code_block_content.append(line)
                else:
                    current_text.append(line)

            # Render any remaining text
            if current_text:
                st.markdown('\n'.join(current_text))

            # If we're still in a code block, render it
            if in_code_block and code_block_content:
                st.code('\n'.join(code_block_content), language=language)

        return True
    except Exception as e:
        st.error(f"Error rendering markdown: {str(e)}")
        # Fallback to code display if markdown rendering fails
        st.text(markdown_text[:1000] + "..." if len(markdown_text) > 1000 else markdown_text)
        return False

