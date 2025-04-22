# Markdown Converter UI

![Markdown Converter UI](docs/screenshots/app_screenshot.png)

A streamlined web interface for converting various file formats to Markdown using the [MarkItDown](https://github.com/microsoft/markitdown/) library from Microsoft.

## 🚀 Features

- **Simple Upload Interface**: Drag and drop or select files for conversion
- **Multiple Format Support**: Convert various document formats (DOCX, PDF, HTML, etc.) to clean Markdown
- **Live Preview**: Instantly see the converted Markdown in the browser
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

### Docker Deployment

1. Create a Dockerfile in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
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
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
├── README.md           # This documentation
└── docs/               # Documentation assets
    └── screenshots/    # Application screenshots
```

### Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Customization

You can customize the application by:

- Adjusting the `MAX_FILE_SIZE_MB` constant in app.py
- Modifying the CSS styles for better UI appearance
- Adding additional conversion options in the sidebar

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown/) for the conversion library
- Streamlit for the web application framework

## 📸 Screenshots

### Main Interface
![Main Interface](docs/screenshots/main_interface.png)

### File Conversion
![File Conversion](docs/screenshots/conversion_process.png)

### Preview Result
![Preview Result](docs/screenshots/preview_result.png)
