from flask import Flask, send_file,request
from scheduleOCR import extract_grades
import requests
import urllib.request as requesturllib
import json

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
        
        

@app.route('/schedule', methods=['POST'])
def process_schedule():
    # Extract the grade and PDF file data from the tuple
    body = request.data
    data = json.loads(body)

    # Get the pdf_url value
    pdf_url = data['pdf_url']
    print(pdf_url)
    grade_data_list = extract_grades(pdf_url)

    # Send each grade and PDF file data to the Node.js server
    if grade_data_list:
        for schedule_tuple in grade_data_list:
            server_url = 'http://localhost:9090/schedule/save'
            send_schedule_to_nodejs_server(schedule_tuple, server_url)
    else:
        print('No grades found in the PDF file.')
    


if __name__ == '__main__':
    app.run()