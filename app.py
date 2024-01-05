import os
from flask import Flask, render_template, request, flash, send_file, redirect, url_for
from PyPDF2 import PdfFileReader, PdfFileWriter
import tempfile
import shutil
import zipfile


app = Flask(__name__)
app.secret_key = 'codewithdark'

# Function to split a PDF into multiple pages and return them as a ZIP file
# Function to split a PDF into multiple pages and return them as a ZIP file
def split_pdf(input_pdf, output_directory):
    pdf = PdfFileReader(input_pdf)
    output_files = []

    # Create a temporary directory to store the split PDF pages
    temp_dir = tempfile.mkdtemp()

    try:
        for page_num in range(len(pdf.pages)):  # Use len(reader.pages) to get the number of pages
            page = pdf.pages[page_num]
            pdf_writer = PdfFileWriter()
            pdf_writer.add_page(page)

            output_file = os.path.join(temp_dir, f"page_{page_num + 1}.pdf")
            output_files.append(output_file)

            with open(output_file, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

        # Create a ZIP file containing the split PDF pages
        zip_filename = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))

        return zip_filename

    finally:
        # Clean up the temporary directory and files
        shutil.rmtree(temp_dir, ignore_errors=True)


# Route to start a download (you can add specific file preparation code here)
@app.route('/start_download', methods=['GET'])
def start_download():
    flash("Download started.", 'info')
    return redirect(url_for('index', download_started=1))

# Route to render the HTML form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for handling PDF merging
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    pdfs = request.files.getlist('pdfs')
    if len(pdfs) < 2:
        flash("Select at least two PDF files to merge.", 'error')
    else:
        merger = PdfFileWriter()
        for pdf in pdfs:
            pdf_reader = PdfFileReader(pdf)
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                merger.addPage(page)

        output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(output_pdf.name, "wb") as output_pdf_file:
            merger.write(output_pdf_file)

        # Return the merged PDF for download
        return send_file(output_pdf.name, as_attachment=True, download_name='merged.pdf')

    flash("File merging failed. Select at least two PDF files.", 'error')
    return render_template('index.html')

# Route for converting text to PDF
@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    text_file = request.files['text_file']
    if not text_file:
        flash("Select a text file to convert.", 'error')
    else:
        # Create a PDF instance using FPDF
        pdf = FPDF()
        pdf.add_page()

        # Read the text content from the text file
        text_content = text_file.read().decode("utf-8")

        # Set font and font size (you can customize these)
        pdf.set_font("Arial", size=12)

        # Add the text content to the PDF
        pdf.multi_cell(0, 10, text_content)

        # Generate a unique PDF filename
        output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(output_pdf.name)

        # Return the PDF file for download
        return send_file(output_pdf.name, as_attachment=True, download_name='converted.pdf')

    flash("File converting failed. Select a text file.", 'error')
    return render_template('index.html')

# Route for splitting a PDF and returning as a ZIP file
@app.route('/split', methods=['POST'])
def split_and_download():
    pdf_to_split = request.files['pdf_to_split']
    if not pdf_to_split:
        flash("Select a PDF file to split.", 'error')
        return render_template('index.html')

    # Split the PDF and get the path to the ZIP file
    zip_filename = split_pdf(pdf_to_split, "split_pages")

    # Return the ZIP file for download
    return send_file(zip_filename, as_attachment=True, download_name='split_pages.zip')

if __name__ == '__main__':
    app.run(debug=True)
