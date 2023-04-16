import PyPDF2
import io
from flask import Flask, send_file
from scheduleOCR import extract_grade_page_num

app = Flask(__name__)

@app.route('/get_grade_pdf/<grade>')
def get_grade_pdf(grade):
    pdf_file_path = r"C:\Users\MSI\Downloads\Emploi du temps Semaine 30-01-2023.pdf"

    # Extract the page number where the grade is found
    page_num = extract_grade_page_num(pdf_file_path, grade)

    # Check if the grade is found in the PDF file
    if page_num is None:
        return f'Grade {grade} not found in the PDF file'

    # Open the PDF file in read-binary mode
    with open(pdf_file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Get the page that contains the grade
        page = pdf_reader.getPage(page_num)

        # Create a new PDF file writer object
        pdf_writer = PyPDF2.PdfFileWriter()

        # Add the page to the PDF file writer object
        pdf_writer.addPage(page)

        # Create a new in-memory file object
        pdf_file_object = io.BytesIO()

        # Write the PDF content to the in-memory file object
        pdf_writer.write(pdf_file_object)

        # Move the file pointer to the beginning of the file object
        pdf_file_object.seek(0)

        # Return the PDF file data as a response
        return pdf_file_object.getvalue()

if __name__ == '__main__':
    app.run()