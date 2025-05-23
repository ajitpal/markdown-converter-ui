# Markdown Converter UI

![Markdown Converter UI](docs/screenshots/app_screenshot.png)

A streamlined web interface for converting various file formats to Markdown using the [MarkItDown](https://github.com/microsoft/markitdown/) library from Microsoft. Transform any document into clean, LLM-ready Markdown with this powerful conversion tool.

## 🧠 LLM-Ready Document Conversion

Markdown Converter UI leverages Microsoft's MarkItDown, an open-source server that transforms virtually any document into clean, LLM-ready Markdown:

- **Universal Format Support**: Convert PDFs, PowerPoint presentations, Word documents, audio files, and even images into consistent Markdown
- **Advanced Processing**: Extracts EXIF data, performs OCR on images, generates transcripts from audio, and adds AI-generated image captions
- **LLM Integration**: Seamlessly prepare documents for local LLM applications like Cursor, Windsurf, Cline, and Claude Desktop
- **AI Workflow Optimization**: Instantly prepare data for fine-tuning and RAG (Retrieval-Augmented Generation) workflows without manual cleanup
- **Scalable Document Processing**: Batch support for processing multiple documents simultaneously

This tool effectively serves as an AI data engineer in your workflow, turning any knowledge base into prompt-ready content for AI assistants.

## 🚀 Features

- **Professional UI**: Clean, modern interface with intuitive controls
- **Simple Upload Interface**: Drag and drop or select files for conversion
- **Multiple Format Support**: Convert various document formats (DOCX, PDF, HTML, etc.) to clean Markdown
- **Live Preview**: Instantly see the converted Markdown in the browser with vertical scrolling for large documents
- **Download Options**: Save the converted Markdown to your local machine
- **Batch Processing**: Convert multiple files at once with tab interface
- **Error Handling**: Clear feedback when conversion issues occur
- **Large File Support**: Process files up to 50MB with progress indicators
- **Automatic Cleanup**: Temporary files are automatically removed after 2 hours

## 📋 Requirements

- Python 3.8+
- Streamlit
- MarkItDown library from Microsoft with extended dependencies

## 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ajitpal/markdown-converter-ui.git
   cd markdown-converter-ui
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # On Windows
   .\venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt

   # Install MarkItDown with all optional dependencies (PDF, DOCX, etc. support)
   pip install "markitdown[all]"
   ```

## 💻 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Use the application:
   - Upload one or more files using the file upload interface
   - Adjust conversion settings in the sidebar if needed
   - View converted files in the preview tab
   - Download the converted Markdown files using the download buttons
   - Use the clean, structured Markdown with your favorite LLM tools

4. LLM Integration:
   - Feed the converted Markdown directly into LLM applications
   - Use for training data preparation in fine-tuning workflows
   - Build RAG systems with the consistently formatted content
   - Create knowledge bases that are instantly AI-ready

![App Workflow](docs/screenshots/app_workflow.png)

## 🚢 Deployment Options

### Local Deployment

Run the app locally as described in the Usage section above.

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app with the following settings:
   - Main file path: `app.py`
   - Python version: 3.8 or higher
   - Requirements: `requirements.txt`
   - Advanced settings > Packages: `packages.txt`

**Important Note for Streamlit Cloud:**

If you encounter PDF conversion errors like `MissingDependencyException`, ensure that:

1. Your `requirements.txt` includes `markitdown[all]>=0.1.0` (not just `markitdown>=0.1.0`)
2. You have a `packages.txt` file with the necessary system dependencies:
   ```
   poppler-utils
   tesseract-ocr
   libreoffice
   ffmpeg
   ```
3. If issues persist, you may need to use the Streamlit secrets management to set environment variables for the PDF processing libraries.

### Docker Deployment

1. Create a Dockerfile in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Explicitly install MarkItDown with all dependencies
RUN pip install "markitdown[all]"

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

2. Build and run the Docker container:

```bash
docker build -t markdown-converter-ui .
docker run -p 8501:8501 markdown-converter-ui
```

3. Access the application at http://localhost:8501

### AWS/Azure Deployment

For cloud deployments on AWS, Azure, or GCP:

1. Build the Docker container as shown above
2. Push the container to a container registry (ECR, ACR, etc.)
3. Deploy using a service like:
   - AWS App Runner
   - Azure Container Instances
   - Google Cloud Run

Each service will have specific steps for deployment from a container.

## 🛠️ Development

### Project Structure

```
markdown-converter-ui/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── src/                    # Source code directory
│   ├── main.py            # Core application logic
│   ├── config.py          # Configuration settings
│   ├── ui/                # UI components
│   │   ├── components.py  # Reusable UI components
│   │   ├── styles.py      # CSS styles
│   │   └── layout.py      # Page layout configuration
│   └── utils/             # Utility functions
│       ├── cleanup.py     # Temporary file cleanup
│       ├── file_helpers.py # File handling utilities
│       └── markdown_converter.py # Markdown conversion logic
├── static/                # Static assets
├── tests/                 # Test files
├── docs/                  # Documentation
└── venv/                  # Virtual environment (not in git)
```

### Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Customization

You can customize the application by:

- Adjusting the `MAX_FILE_SIZE_MB` constant in src/config.py
- Modifying the CSS styles in src/ui/styles.py for UI appearance
- Changing the max height for preview sections by editing the `.preview-container` and `.stCodeBlock` CSS classes
- Adding additional conversion options in the sidebar
- Updating the header and footer in src/ui/components.py

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown/) for the powerful conversion library that makes documents LLM-ready
- Streamlit for the web application framework
- The AI and LLM community for inspiring tools that bridge the gap between traditional documents and AI-ready content

## 📸 Screenshots

### Main Interface
![Main Interface](docs/screenshots/main_interface.png)

### File Conversion
![File Conversion](docs/screenshots/conversion_process.png)

### Preview Result
![Preview Result](docs/screenshots/preview_result.png)

## Troubleshooting

### Common Issues

1. **Import Errors**
   - If you see import errors, make sure you're running the application from the project root directory
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that your Python path includes the project root

2. **File Conversion Issues**
   - Verify that the input file format is supported
   - Check file size limits (default is 50MB)
   - Ensure you have write permissions in the temporary directory

3. **PDF Conversion Issues**
   - If you see `MissingDependencyException` errors, ensure you've installed MarkItDown with PDF support:
     ```bash
     pip install "markitdown[all]"
     # or specifically for PDF
     pip install "markitdown[pdf]"
     ```
   - Make sure you have the necessary system dependencies installed:
     - On Ubuntu/Debian: `sudo apt-get install poppler-utils tesseract-ocr libreoffice ffmpeg`
     - On macOS with Homebrew: `brew install poppler tesseract libreoffice ffmpeg`
     - On Windows: Install the appropriate binaries and ensure they're in your PATH
   - For Streamlit Cloud deployment, ensure your `packages.txt` file includes these dependencies
   - Check that your PDF files are not corrupted or password-protected

4. **UI Issues**
   - Clear your browser cache if the UI is not loading properly
   - Ensure you're using a modern browser (Chrome, Firefox, or Edge recommended)
   - Check the browser console for any JavaScript errors
   - If the "Clean All" button is not visible after uploading files, try refreshing the page
   - For large documents, use the vertical scrolling in the preview and raw sections

### Getting Help

If you encounter issues not covered here:
1. Check the application logs for detailed error messages
2. Review the documentation in the `docs/` directory
3. Open an issue on the project's GitHub repository
