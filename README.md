# PDF Merger and Text to PDF Converter

This Flask application facilitates PDF-related operations such as merging, converting text to PDF, and splitting PDFs. It offers a user-friendly interface and utilizes the PyPDF2 library for PDF manipulation.

## Features

- **Merge PDF Files:** Combine multiple PDFs into a single document for efficient document management.
- **Convert Text to PDF:** Transform plain text documents into professionally formatted PDFs.
- **Split PDF:** Break down large PDFs into individual pages and download them as a ZIP file.

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Open your browser and visit `http://localhost:5000` to access the application.

## How to Use

- **Merge PDF Files:**
  1. Click on the "Merge PDF Files" section.
  2. Select at least two PDF files to merge.
  3. Click "Merge" and download the combined PDF.

- **Convert Text to PDF:**
  1. Navigate to the "Convert Text to PDF" section.
  2. Upload a text file.
  3. Click "Convert" and download the resulting PDF.

- **Split PDF:**
  1. Access the "Split PDF" section.
  2. Upload a PDF file to split.
  3. Click "Split" and download the pages as a ZIP file.

## Notes

- This application uses Flask, a Python web framework, and PyPDF2 for PDF manipulation.
- Ensure you have Python installed on your system.
