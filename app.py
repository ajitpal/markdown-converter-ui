import os
import tempfile
from io import BytesIO
import base64
import streamlit as st
from markitdown import convert
from markitdown.handlers import FileHandler

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
    }
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #888;
        font-size: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# Helper function to convert file to markdown
def convert_to_markdown(file_path, options=None):
    """Convert a file to markdown using markitdown library"""
    try:
        handler = FileHandler(file_path)
        result = convert(handler, options=options)
        return result
    except Exception as e:
        st.error(f"Error converting file: {str(e)}")
        return None

# Main app functionality
if uploaded_files:
    st.markdown("---")
    
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
            st.write(f"Processing: **{file.name}**")
            
            # Save uploaded file to temp directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                tmp_file.write(file.getvalue())
                temp_file_path = tmp_file.name
            
            try:
                # Create a progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                status_text.text("Starting conversion...")
                progress_bar.progress(25)
                
                # Convert file to markdown
                status_text.text("Converting to Markdown...")
                markdown_content = convert_to_markdown(temp_file_path, options=conversion_options)
                progress_bar.progress(75)
                
                if markdown_content:
                    # Update progress
                    status_text.text("Conversion complete!")
                    progress_bar.progress(100)
                    
                    # Display tabs for preview and raw markdown
                    preview_tabs = st.tabs(["Preview", "Raw Markdown"])
                    
                    with preview_tabs[0]:
                        st.markdown(markdown_content)
                    
                    with preview_tabs[1]:
                        st.code(markdown_content, language="markdown")
                    
                    # Download button
                    output_filename = os.path.splitext(file.name)[0] + ".md"
                    st.markdown(
                        get_download_link(markdown_content, output_filename, f"Download {output_filename}"),
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Failed to convert file. Please check if the file format is supported.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
else:
    # Display instructions when no files are uploaded
    st.info("Please upload one or more files to convert them to Markdown.")
    
    # Example section
    with st.expander("See Example"):
        st.markdown("""
        ### Example Markdown Output
        
        # Sample Document
        
        This is a paragraph with **bold** and *italic* text.
        
        ## Section Heading
        
        - List item 1
        - List item 2
        - List item 3
        
        ### Code Example
        
        ```python
        def hello_world():
            print("Hello, World!")
        ```
        
        > This is a blockquote with important information.
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

