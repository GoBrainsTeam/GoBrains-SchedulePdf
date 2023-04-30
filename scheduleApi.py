from flask import Flask, send_file,request
from scheduleOCR import extract_grades
import requests
import urllib.request as requesturllib
import json

app = Flask(__name__)


def send_schedule_to_nodejs_server(schedule_tuple, server_url,sendNotif):
    # Extract the grade and PDF file data from the tuple
    grade, pdf_schedule = schedule_tuple

    # Send a POST request to the server with the grade and PDF file data
    files = {'schedule': (f'{grade.lower()}.pdf', pdf_schedule)}
    data = {'sendNotif': sendNotif}
    print(sendNotif)
    response = requests.post(server_url, data=data , files=files)
    print(f'Request body: {data}')
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
    sendNotif = False
    # Get the pdf_url value
    pdf_url = data['pdf_url']
    print(pdf_url)
    grade_data_list = extract_grades(pdf_url)

    # Send each grade and PDF file data to the Node.js server
    if grade_data_list:
        for i, schedule_tuple in enumerate(grade_data_list):
            server_url = 'http://localhost:9090/schedule/save'           
            if i == len(grade_data_list) - 1:
                sendNotif = True
            send_schedule_to_nodejs_server(schedule_tuple, server_url,sendNotif)
            
    else:
        print('No grades found in the PDF file.')
    return "Schedule send to nodeJs server"
    


if __name__ == '__main__':
    app.run()