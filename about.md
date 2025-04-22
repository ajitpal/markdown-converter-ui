# About Me - Markdown Converter UI

I've developed a streamlined web interface that transforms virtually any document into clean, LLM-ready Markdown using Microsoft's MarkItDown. This tool serves as an AI data engineer in your workflow, converting PDFs, PowerPoint presentations, Word documents, audio files, and even images into consistent Markdown format.

## Key Features
- **Universal Format Support**: Handles multiple document types with a simple drag-and-drop interface
- **Advanced Processing**: Extracts EXIF data, performs OCR, generates transcripts, and adds AI-generated image captions
- **LLM Integration**: Prepares documents for AI applications like Cursor, Windsurf, Cline, and Claude Desktop
- **Optimized UI**: Clean interface with live preview, vertical scrolling for large documents, and batch processing
- **AI Workflow Ready**: Instantly prepares data for fine-tuning and RAG workflows without manual cleanup

## Technical Implementation
- Built with Python and Streamlit for a responsive web interface
- Implemented fixed-height scrollable containers for both Preview and Raw tabs
- Added horizontal scrolling for file tabs when many files are uploaded
- Ensured proper vertical scrolling to prevent page stretching
- Optimized CSS for consistent styling and professional appearance

This project bridges the gap between traditional documents and AI-ready content, making it easier to turn any knowledge base into prompt-ready material for AI assistants.

## Why I Built This
I wanted to eliminate the tedious process of manually preparing documents for LLMs. This tool automates document ingestion at scale, allowing users to focus on leveraging AI rather than data preparation. It's like having an AI data engineer in your pocket - 100% open source with no strings attached.
