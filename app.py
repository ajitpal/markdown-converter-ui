import os
import tempfile
from io import BytesIO
import base64
import streamlit as st
import logging
import threading
import time
import datetime
import shutil
import uuid
from pathlib import Path
from markitdown import MarkItDown, FileConversionException, DocumentConverterResult

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE_MB = 50  # Maximum allowed file size in MB
FILE_EXPIRY_HOURS = 2  # Files will be deleted after this many hours
TEMP_DIR = Path(tempfile.gettempdir()) / "markdown-converter-ui"

# Create temp directory if it doesn't exist
TEMP_DIR.mkdir(exist_ok=True, parents=True)

# Dictionary to track temporary files with their creation time
temp_files = {}

# Page configuration
st.set_page_config(
    page_title="Markdown Converter UI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.5rem;
    }
    .download-button {
        margin-top: 1rem;
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
    .download-button:hover {
        background-color: #45a049;
    }
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #888;
        font-size: 0.8rem;
    }
    /* Custom styling for markdown content */
    .preview-container {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
        padding: 20px;
        background-color: #f9f9f9;
        overflow-y: auto;
        max-height: 600px;
        margin-bottom: 20px;
    }
    .markdown-preview h1 {
        border-bottom: 1px solid #ddd;
        padding-bottom: 10px;
    }
    .markdown-preview h2 {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .markdown-preview h3, .markdown-preview h4 {
        margin-top: 15px;
    }
    .markdown-preview code {
        background-color: #f0f0f0;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: monospace;
    }
    .markdown-preview pre {
        background-color: #f6f8fa;
        padding: 16px;
        border-radius: 6px;
        overflow-x: auto;
    }
    .markdown-preview blockquote {
        border-left: 4px solid #ddd;
        padding-left: 16px;
        color: #666;
        margin-left: 0;
    }
    .markdown-preview table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    .markdown-preview table, .markdown-preview th, .markdown-preview td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .markdown-preview th {
        background-color: #f2f2f2;
        text-align: left;
    }
    .file-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        background-color: #f2f2f2;
    }
    .error-message {
        color: #721c24;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-message {
        color: #856404;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    /* Button row styling */
    .button-row {
        display: flex;
        gap: 10px;
        margin: 10px 0;
        align-items: center;
    }
    .clear-button {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    /* Action button styling */
    .action-area {
        display: flex;
        justify-content: space-between;
        margin: 10px 0;
        padding: 10px;
        background-color: #f7f7f7;
        border-radius: 5px;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state initialization for clear functionality
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = False

# Function to clear all and reset
def clear_all_files():
    st.session_state.processed_files = False
    st.experimental_rerun()

# App header
st.title("Markdown Converter UI")
st.markdown("Convert various file formats to clean Markdown using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown/) library.")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This application allows you to convert various file formats to Markdown.
        
        ### Supported Formats
        - Word Documents (.docx)
        - HTML files (.html)
        - PDF documents (.pdf)
        - And more...
        
        ### How to Use
        1. Upload one or more files
        2. Convert to Markdown
        3. Preview the result
        4. Download the Markdown file
        """
    )
    
    st.header("Settings")
    include_images = st.checkbox("Include images", value=True, help="When enabled, images from the original document will be embedded in the Markdown.")
    preserve_tables = st.checkbox("Preserve tables", value=True, help="When enabled, tables will be preserved as Markdown tables.")

    st.markdown("---")
    st.markdown("Built with Streamlit and [MarkItDown](https://github.com/microsoft/markitdown/)")

# File upload section
st.header("Upload Files")
uploaded_files = st.file_uploader(
    "Choose files to convert", 
    accept_multiple_files=True,
    type=["docx", "html", "pdf", "txt", "md", "rtf"]
)

# Helper function to generate download link
def get_download_link(content, filename, text):
    """Generate a download link for the content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-button">{text}</a>'

# Helper function to format file size
def format_file_size(size_bytes):
    """Format file size in a human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

# Cleanup function for temporary files
def cleanup_expired_files():
    """Clean up temporary files that are older than the expiry time"""
    while True:
        try:
            current_time = datetime.datetime.now()
            files_to_remove = []
            
            # Check all tracked files
            for file_path, creation_time in list(temp_files.items()):
                time_diff = current_time - creation_time
                # Check if file is older than expiry time
                if time_diff.total_seconds() > FILE_EXPIRY_HOURS * 3600:
                    try:
                        if os.path.exists(file_path):
                            os.unlink(file_path)
                            logger.info(f"Deleted expired file: {file_path}")
                        files_to_remove.append(file_path)
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {str(e)}")
            
            # Remove deleted files from tracking dict
            for file_path in files_to_remove:
                temp_files.pop(file_path, None)
                
            # Also clean up any files in the temp directory that are not being tracked
            try:
                for file_path in TEMP_DIR.glob("*"):
                    if str(file_path) not in temp_files and file_path.is_file():
                        creation_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                        time_diff = current_time - creation_time
                        if time_diff.total_seconds() > FILE_EXPIRY_HOURS * 3600:
                            file_path.unlink()
                            logger.info(f"Deleted untracked expired file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up directory: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error in cleanup thread: {str(e)}")
            
        # Sleep for 15 minutes before next cleanup
        time.sleep(15 * 60)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_expired_files, daemon=True)
cleanup_thread.start()
# Helper function to safely render markdown
def render_markdown(markdown_text):
    """Safely render markdown content with proper formatting"""
    try:
        # Create a container with proper styling
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        
        # Split the markdown into code blocks and regular text
        lines = markdown_text.split('\n')
        in_code_block = False
        current_block = []
        
        for line in lines:
            if line.startswith('```'):
                # Toggle code block state
                if in_code_block:
                    # End of code block - render accumulated lines as code
                    code_content = '\n'.join(current_block)
                    language = line[3:].strip() if len(line) > 3 else ""
                    st.code(code_content, language=language)
                    current_block = []
                else:
                    # Start of code block - render accumulated lines as markdown
                    if current_block:
                        st.markdown('\n'.join(current_block))
                        current_block = []
                in_code_block = not in_code_block
            else:
                current_block.append(line)
        
        # Render any remaining content
        if current_block:
            if in_code_block:
                st.code('\n'.join(current_block))
            else:
                st.markdown('\n'.join(current_block))
        
        st.markdown('</div>', unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"Error rendering markdown: {str(e)}")
        # Fallback to code display if markdown rendering fails
        st.text(markdown_text[:1000] + "..." if len(markdown_text) > 1000 else markdown_text)
        return False
        return False
# Helper function to convert file to markdown
def convert_to_markdown(file_path, options=None, status_placeholder=None, progress_bar=None):
    """Convert a file to markdown using markitdown library"""
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

# Main app functionality
if 'clear_button' not in st.session_state:
    st.session_state.clear_button = False

# Add Clear All button at the top if files have been processed
if st.session_state.processed_files:
    if st.button("Clear All Files", key="clear_all", type="primary"):
        clear_all_files()

if uploaded_files:
    st.markdown("---")
    
    # Mark that files have been processed
    st.session_state.processed_files = True
    
    # Create tabs for each file
    file_tabs = st.tabs([f.name for f in uploaded_files])
    
    # Options for conversion
    conversion_options = {
        "include_images": include_images,
        "preserve_tables": preserve_tables,
    }
    
    # Process each file
    for i, file in enumerate(uploaded_files):
        with file_tabs[i]:
            # Display file info
            file_size = len(file.getvalue())
            file_size_formatted = format_file_size(file_size)
            st.markdown(f"""
            <div class="file-info">
                <span><strong>File:</strong> {file.name}</span>
                <span><strong>Size:</strong> {file_size_formatted}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Check file size before processing
            if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"File exceeds size limit of {MAX_FILE_SIZE_MB}MB. Your file is {file_size / (1024 * 1024):.1f}MB.")
                continue
                
            # Save uploaded file to temp directory with a unique name
            unique_id = str(uuid.uuid4())
            file_ext = os.path.splitext(file.name)[1]
            temp_file_name = f"{unique_id}{file_ext}"
            temp_file_path = os.path.join(TEMP_DIR, temp_file_name)
            
            with open(temp_file_path, 'wb') as f:
                f.write(file.getvalue())
            
            # Add to tracked files with creation time
            temp_files[temp_file_path] = datetime.datetime.now()
            logger.info(f"Created temporary file: {temp_file_path}")
            
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
                    output_filename = os.path.splitext(file.name)[0] + ".md"
                    
                    # Create action area with download button at top
                    st.markdown(
                        f"""
                        <div class="action-area">
                            <span><strong>Conversion successful!</strong> File is ready to download.</span>
                            {get_download_link(markdown_content, output_filename, f"Download {output_filename}")}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Display tabs for preview and raw markdown
                    preview_tabs = st.tabs(["Preview", "Raw Markdown"])
                    
                    with preview_tabs[0]:
                        # Use the improved markdown rendering function
                        success = render_markdown(markdown_content)
                        if not success:
                            st.info("Preview may not display properly. Please check the Raw Markdown tab.")
                    
                    with preview_tabs[1]:
                        # Button row for actions
                        col1, col2 = st.columns([1, 6])
                        with col1:
                            if st.button("Copy", key=f"copy_{i}"):
                                st.success("Markdown copied to clipboard!")
                        with col2:
                            # Repeat download button for convenience
                            st.markdown(
                                get_download_link(markdown_content, output_filename, f"Download {output_filename}"),
                                unsafe_allow_html=True
                            )
                        
                        # Display raw markdown with syntax highlighting
                        st.code(markdown_content, language="markdown")
                    )
                else:
                    st.error("Failed to convert file. Please check if the file format is supported.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
            finally:
                # Don't delete the file immediately - let the cleanup thread handle it
                # This ensures files aren't deleted before download completes
                pass
else:
    # Display instructions when no files are uploaded
    st.info("Please upload one or more files to convert them to Markdown.")
    
    # Example section
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
        - Converting documentation to Markdown
        - Preparing content for websites that use Markdown
        - Extracting text from PDFs in a clean, structured format
        """)

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Markdown Converter UI - Powered by Microsoft's MarkItDown</p>
        <p>Copyright © 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)

