"""
CSS styles for the Markdown Converter UI.
"""

import streamlit as st


def apply_styles():
    """
    Apply CSS styles to the application.
    This includes styles for the layout, header, markdown preview, and UI controls.
    """
    st.markdown(
        """
        <style type="text/css">
        /* Layout styles */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0.5rem;
        }
        .main-content {
            margin-top: 20px;
        }

        /* App header styles */
        .app-header {
            background-color: #ffffff;
            padding: 25px 30px 20px 30px;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            align-items: center;
            border-top: 4px solid #4285f4;
            border-left: 1px solid #eaeaea;
            border-right: 1px solid #eaeaea;
            border-bottom: 1px solid #eaeaea;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 15px;
            padding-bottom: 12px;
            border-bottom: 1px solid #eaeaea;
            width: 100%;
        }
        .app-summary {
            text-align: center;
            color: #333;
            max-width: 800px;
            margin: 15px auto 5px auto;
            line-height: 1.5;
            font-size: 1.2rem;
            padding: 0 10px;
            font-weight: 500;
        }

        .app-summary .highlight {
            color: #4285f4;
            font-weight: 600;
        }

        .app-description {
            text-align: center;
            color: #444;
            max-width: 800px;
            margin: 12px auto 0 auto;
            line-height: 1.5;
            font-size: 1rem;
            padding: 0 10px;
        }
        .logo-text {
            font-size: 2.2rem;
            font-weight: 600;
            margin-bottom: 4px;
            color: #222;
            display: flex;
            align-items: center;
            justify-content: center;
            letter-spacing: -0.3px;
        }
        .logo-icon {
            font-size: 2.4rem;
            margin-right: 10px;
            color: #4285f4;
        }
        .app-tagline {
            font-size: 1.1rem;
            color: #555;
            margin-top: 4px;
            font-weight: 400;
            letter-spacing: 0.2px;
        }
        .header-separator {
            width: 100%;
            height: 1px;
            background-color: #eaeaea;
            margin: 10px 0;
        }

        /* Button and control styles */
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
        .action-area {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background-color: #f7f7f7;
            border-radius: 5px;
            align-items: center;
        }

        /* Markdown preview styles */
        .preview-container {
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            padding: 20px;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }

        /* Style for code blocks in raw section */
        .stCodeBlock {
            max-height: none;
        }

        /* Remove forced scrolling on vertical blocks */
        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
            max-height: none;
            overflow-y: visible;
        }

        /* Ensure the main content doesn't stretch */
        .main .block-container {
            max-width: 100%;
            padding-bottom: 5rem;
            padding-top: 1rem;
        }

        /* Fix for Streamlit's markdown rendering */
        .element-container .stMarkdown {
            overflow-y: visible;
        }

        /* Scrollable containers for preview and raw content */
        .preview-container, .raw-container {
            height: 500px;
            overflow-y: auto;
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            white-space: pre-wrap;
        }

        /* Specific styling for raw container */
        .raw-container {
            background-color: #f5f5f5;
        }

        /* Style for pre tag in raw container */
        .raw-container pre {
            margin: 0;
            font-family: 'Courier New', Courier, monospace;
            color: #333;
        }

        /* Add horizontal scrolling for file tabs */
        .stTabs [role="tablist"] {
            flex-wrap: nowrap;
            overflow-x: auto;
            white-space: nowrap;
        }

        /* Ensure tab content doesn't stretch the page */
        .stTabs [data-baseweb="tab-panel"] {
            overflow: visible;
            margin-bottom: 20px;
        }

        /* Ensure the main content area is properly contained */
        .main .block-container {
            padding-bottom: 2rem;
            max-width: 100%;
        }

        /* Additional tab panel styling */
        .stTabs {
            margin-bottom: 30px;
        }

        /* Add horizontal scrolling for file tabs */
        .stTabs [role="tablist"] {
            flex-wrap: nowrap;
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: thin;
        }

        /* Style the scrollbar for the tabs */
        .stTabs [role="tablist"]::-webkit-scrollbar {
            height: 5px;
        }

        .stTabs [role="tablist"]::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        .stTabs [role="tablist"]::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        .preview-markdown-container p {
            margin-bottom: 1em;
            line-height: 1.6;
        }
        .preview-markdown-container h1,
        .preview-markdown-container h2,
        .preview-markdown-container h3 {
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        .preview-markdown-container pre {
            padding: 1em;
            background-color: #f6f8fa;
            border-radius: 6px;
            margin-bottom: 1em;
        }
        .preview-markdown-container blockquote {
            border-left: 4px solid #ddd;
            padding-left: 1em;
            margin-left: 0;
            color: #666;
        }
        .preview-container h1, .preview-container h2, .preview-container h3 {
            margin-top: 1em;
            margin-bottom: 0.5em;
            font-weight: 600;
        }
        .preview-container h1 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }
        .preview-container p {
            margin-bottom: 1em;
            line-height: 1.6;
        }
        .preview-container ul, .preview-container ol {
            margin-bottom: 1em;
            padding-left: 2em;
        }
        .preview-container blockquote {
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
        }
        .preview-container pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 6px;
        }
        .preview-container code {
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
        }
        .preview-container img {
            max-width: 100%;
            box-sizing: content-box;
            background-color: #fff;
        }

        /* UI feedback styles */
        .file-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            background-color: #f2f2f2;
        }

        /* Success action area with download button */
        .action-area {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Download button styling */
        .download-button {
            display: inline-block;
            padding: 8px 16px;
            background-color: #28a745;
            color: white !important;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            transition: background-color 0.3s;
            border: none;
            cursor: pointer;
        }

        .download-button:hover {
            background-color: #218838;
            text-decoration: none;
        }

        .download-button.error {
            background-color: #dc3545;
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

        /* Footer styles */
        .footer {
            margin-top: 3rem;
            text-align: center;
            color: #888;
            font-size: 0.8rem;
            padding: 15px 0;
            border-top: 1px solid #eaeaea;
            background-color: #f8f9fa;
            width: 100%;
            clear: both;
            position: relative;
            z-index: 10;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

