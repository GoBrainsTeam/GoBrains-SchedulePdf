from flask import Flask, send_file
from scheduleOCR import extract_grades
import requests

app = Flask(__name__)


def send_schedule_to_nodejs_server(schedule_tuple, server_url):
    # Extract the grade and PDF file data from the tuple
    grade, pdf_schedule = schedule_tuple

    # Send a POST request to the server with the grade and PDF file data
    files = {'schedule': (f'{grade.lower()}.pdf', pdf_schedule)}
    
    response = requests.post(server_url, files=files)

    # Check if the request was successful
    if response.ok:
        print(f'Schedule for grade {grade} sent to Node.js server.')
    else:
        print(f'Error sending schedule for grade {grade} to Node.js server.')


# Get the list of tuples of grade and PDF file data
pdf_file_path = r"C:\Users\MSI\Downloads\Emploi du temps Semaine 30-01-2023.pdf"
grade_data_list = extract_grades(pdf_file_path)

# Send each grade and PDF file data to the Node.js server
if grade_data_list:
    for schedule_tuple in grade_data_list:
        server_url = 'http://localhost:9090/schedule/save'
        send_schedule_to_nodejs_server(schedule_tuple, server_url)
else:
    print('No grades found in the PDF file.')


if __name__ == '__main__':
    app.run()