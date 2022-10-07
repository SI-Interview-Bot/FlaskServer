'''
Used to listen for webhooks from Jira on Orion to update InterviewBot.
'''

# Standard imports
import json
from sys import argv, stdout

# Non-standard imports
from flask import Flask, request

app = Flask(__name__)

@app.route('/issue-update', methods=['POST'])
def parseData():
    stdout.write(f"[+] Parsing data:\n")

    newJSONObject = dict()

    ################
    # Parse data from POST request
    ################
    data = request.get_data()
    data = json.loads(data)

    ################
    # Parse relevant interview data and create new JSON object to return and POST to a webhook
    ################
    # Expected format: "summary": "firstName lastName"
    newJSONObject['name'] = data['issue']['fields']['summary']
    if not newJSONObject['name']:
        newJSONObject['name'] = "Not Given In JIRA"
    
    # Expected format: "field": "Type of Interview"
    newJSONObject['interviewType'] = data['changelog']['items'][0]['field']
    if not newJSONObject['interviewType']:
        newJSONObject['interviewType'] = "Not Given In JIRA"
    
    # Expected format: "customfield_10003": "2022-10-07T19:30:00.000-0400"
    newJSONObject['dateTime'] = data['issue']['fields']['customfield_10003']
    if not newJSONObject['dateTime']:
        newJSONObject['dateTime'] = "Not Given In JIRA"
        date = "Not Given In JIRA"
        time = "Not Given In JIRA"
    else:
        # Get date from dateTime string
        date = newJSONObject['dateTime'].split('T')[0]
        # Get time from dateTime string
        time = newJSONObject['dateTime'].split('T')[1].split('.')[0]
    # Expected format: "key": "CT-####"
    newJSONObject['JIRATicketNumber'] = data['issue']['key']
    if not newJSONObject['JIRATicketNumber']:
        newJSONObject['JIRATicketNumber'] = "Not Given In JIRA"

    stdout.write(f"JIRA Ticket:    {newJSONObject['JIRATicketNumber']}\n")
    stdout.write(f"Candidate Name: {newJSONObject['name']}\n")
    stdout.write(f"Interview Type: {newJSONObject['interviewType']}\n")
    stdout.write(f"Date: {date}\n")
    stdout.write(f"Time: {time}\n")

    stdout.write(f"[+] Parsing complete.\n")

    return f"{newJSONObject}\n"
