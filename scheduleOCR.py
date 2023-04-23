import PyPDF2
import re
import io
import urllib.request


def extract_grade(text):
    # Define a regular expression pattern to match the class string
    pattern =   r'(?<!\d)0?(?!\d9H)\d+[ -]?[A-Z]+[\dA-Z]*'
    # Search for the pattern in the input text
    match = re.search(pattern, text)

    # If a match is found, return the matched string
    if match:
        return match.group()

    # If no match is found, return None
    else:
        return None
    
    
def extract_grades(pdf_file_path_url):
    # Create a PDF reader object
    pdf_url = pdf_file_path_url
    pdf_file_path, _ = urllib.request.urlretrieve(pdf_url)

    pdf_reader = PyPDF2.PdfFileReader(open(pdf_file_path, 'rb'))

    # Initialize an empty list to store the grade and PDF file data for each page
    grade_data_list = []

    # Loop through each page of the PDF file
    for page_num in range(pdf_reader.getNumPages()):
        # Get the current page of the PDF file
        page = pdf_reader.getPage(page_num)

        # Extract the text from the current page
        text = page.extractText()

        # Extract the class grade from the text
        grade = extract_grade(text)

        # If a grade is found, create a new PDF file with only the current page
        if grade:
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

            # Add the grade and the PDF file data as a tuple to the list
            pdf_schedule = pdf_file_object.getvalue()
            grade_data_list.append((grade, pdf_schedule))

    # If no grade is found, return an empty list
    return grade_data_list
    


