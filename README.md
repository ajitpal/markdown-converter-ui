# Markdown Converter UI

A streamlined web interface for converting various file formats to Markdown using the [MarkItDown](https://github.com/microsoft/markitdown/) library from Microsoft.

## 🚀 Features

- **Simple Upload Interface**: Drag and drop or select files for conversion
- **Multiple Format Support**: Convert various document formats to clean Markdown
- **Live Preview**: Instantly see the converted Markdown in the browser
- **Download Options**: Save the converted Markdown to your local machine
- **Batch Processing**: Convert multiple files at once
- **Error Handling**: Clear feedback when conversion issues occur

## 📋 Requirements

- Python 3.8+
- Streamlit
- MarkItDown library from Microsoft

## 🔧 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/markdown-converter-ui.git
   cd markdown-converter-ui
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Upload files using the provided interface

4. Click "Convert to Markdown" to process the files

5. Preview the converted Markdown directly in the browser

6. Use the download button to save the Markdown file

## 🛠️ Development Setup

1. Follow the installation steps above

2. Install development dependencies:
   ```
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```
   pytest tests/
   ```

4. Make your changes and test locally before submitting a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown/) for the conversion library
- Streamlit for the web application framework

