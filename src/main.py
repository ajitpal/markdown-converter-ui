"""
Main application module for the Markdown Converter UI.
"""

import streamlit as st

from src.config import logger, MAX_FILE_SIZE_MB
from src.utils.cleanup import start_cleanup_thread
from src.utils.file_helpers import save_uploaded_file, get_output_filename
from src.utils.markdown_converter import convert_to_markdown
from src.ui import components, styles
from src.ui.layout import setup_layout


def process_file(file, file_tab, conversion_options):
    """
    Process a file for conversion to markdown.

    Args:
        file: The uploaded file to process
        file_tab: The tab where the file results will be displayed
        conversion_options (dict): Options for the markdown conversion
    """
    from src.utils.file_helpers import validate_file_type
    from src.config import ACCEPTED_FILE_TYPES

    with file_tab:
        # Display file info
        components.file_info(file)

        # Validate file type
        if not validate_file_type(file.name, ACCEPTED_FILE_TYPES):
            st.error(f"File type not supported. Please upload one of the following formats: {', '.join([f'.{ext}' for ext in ACCEPTED_FILE_TYPES])}")
            return

        # Check file size before processing
        file_size = len(file.getvalue())
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"File exceeds size limit of {MAX_FILE_SIZE_MB}MB. Your file is {file_size / (1024 * 1024):.1f}MB.")
            return

        # Save uploaded file to temp directory
        temp_file_path = save_uploaded_file(file)
        if not temp_file_path:
            return

        try:
            # Create a progress bar and status indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Update progress
            status_text.text("Starting conversion...")
            progress_bar.progress(25)

            # Convert file to markdown
            status_text.text("Converting to Markdown...")
            markdown_content = convert_to_markdown(
                temp_file_path,
                options=conversion_options,
                status_placeholder=status_text,
                progress_bar=progress_bar
            )

            if markdown_content:
                # Update progress
                status_text.text("Conversion complete!")
                progress_bar.progress(100)

                # Generate output filename
                output_filename = get_output_filename(file.name)

                # Create action area with download button at top
                components.success_action_area(markdown_content, output_filename)

                # Display tabs for preview and raw markdown
                components.preview_tabs(markdown_content, output_filename, id(file))
            else:
                st.error("Failed to convert file. Please check if the file format is supported.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.exception("Error processing file")


def main():
    """
    Main application function.
    """
    # Apply CSS styles
    styles.apply_styles()

    # Render the header
    components.header()

    # Set up the layout and get components
    settings, uploaded_files, _, file_tabs = setup_layout()  # Using _ to ignore main_content as it's not used here

    # Process conversion settings
    conversion_options = {
        "include_images": settings["include_images"],
        "preserve_tables": settings["preserve_tables"],
    }

    # Process each file if any were uploaded
    if uploaded_files and file_tabs:
        for i, file in enumerate(uploaded_files):
            process_file(file, file_tabs[i], conversion_options)

    # Render footer
    components.footer()


if __name__ == "__main__":
    # Start cleanup thread for temporary files
    cleanup_thread = start_cleanup_thread()

    # Run the main application
    main()

