import PyPDF2

def extract_grade_page_num(pdf_file_path, grade):
    # Open the PDF file in read-binary mode
    with open(pdf_file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Loop through each page of the PDF file
        for page_num in range(pdf_reader.getNumPages()):
            # Get the current page of the PDF file
            page = pdf_reader.getPage(page_num)

            # Extract the text from the current page
            text = page.extractText()

            # Find the position of the grade in the text
            grade_start_pos = text.find(grade)

            # Check if the grade is found in the text
            if grade_start_pos != -1:
                # Return the page number where the grade is found
                return page_num

        # Return None if the grade is not found in any page
        return None


