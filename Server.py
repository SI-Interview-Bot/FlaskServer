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

    # Parse data from POST request
    data = request.get_data()
    data = json.loads(data)

    # Parse relevant interview data and create new JSON object to return and POST to a webhook
    newJSONObject['name'] = data['issue']['summary']
    newJSONObject['interviewType']    = data['changelog']['items'][0]['field']
    newJSONObject['dateTime']       = data['issue']['fields']['customfield_10003']
    newJSONObject['JIRATicketNumber'] = data['issue']['key']
    # TODO customfield_10003 will be used for date/time of interview

    stdout.write(f"[+] name=={newJSONObject['name']}\n")
    stdout.write(f"[+] interviewType=={newJSONObject['interviewType']}\n")
    date = newJSONObject['dateTime'].split('T')[0]
    time = newJSONObject['dateTime'].split('T')[1]
    stdout.write(f"[+] dateTime=={date} at {time}\n")
    stdout.write(f"[+] JIRATicketNumber=={newJSONObject['JIRATicketNumber']}\n")

    return f"[+] OK.\n"
