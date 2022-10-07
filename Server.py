'''
Used to listen for webhooks from Jira on Orion to update InterviewBot.
'''

# Standard imports
import json

# Non-standard imports
from flask import Flask, request

app = Flask(__name__)

'''
parseData          - Takes a JSON Object from a JIRA webhook and parses information to
                     build another JSON Object in response.
IN:  HTTP POST     - Handled by Flask
OUT: newJSONObject - The JSON Object built with JIRA's JSON Object. We parse it here with
                     a specific format expected. Should the returned JSON Object start to
                     look weird, or just straight up useless, it could be that JIRA's
                     JSON Object has changed its formatting in such a way that we can no
                     longer parse it.
'''
@app.route('/issue-update', methods=['POST'])
def parseData():
    # Final JSON object to return
    newJSONObject = dict()

    ################
    # Parse data from POST request
    ################
    data = request.get_data()
    data = json.loads(data)

    ################
    # Parse relevant interview data
    ################

    # Name of candidate
    # Expected format: "summary": "firstName lastName"
    if data['issue']['fields']['summary'].split(" ")[0] is not None:
        newJSONObject['name'] = data['issue']['fields']['summary'].split(" ")[0]

    else:
        newJSONObject['name'] = "Not Given In JIRA"

    # The type of interview: Phone, Face-to-Face, etc.
    # Expected format: "field": "Type of Interview"
    if data['changelog']['items'][0]['field'] is not None:
        newJSONObject['interviewType'] = data['changelog']['items'][0]['field']

    else:
        newJSONObject['interviewType'] = "Not Given In JIRA"

    # MAINTENANCE NOTE: If the date and time are being entered in JIRA and Server.py is
    # producing a JSON object without that data, it could be formatted differently.
    # Server.py is expecting the value of this field to be delimited by a "T". Check if
    # the date time format has changed in the JSON produced by JIRA's webhook and update
    # how we prase that here.
    # Date and time of interview
    try:
        # Expected format: "customfield_10003": "2022-10-07T19:30:00.000-0400"
        newJSONObject['dateTime'] = data['issue']['fields']['customfield_10003']
        # Get date from dateTime string
        date = newJSONObject['dateTime'].split('T')[0]
        # Get time from dateTime string
        time = newJSONObject['dateTime'].split('T')[1].split('.')[0]

    except:
        newJSONObject['dateTime'] = "Not Given In JIRA"
        date = "Not Given In JIRA"
        time = "Not Given In JIRA"

    # Expected format: "key": "CT-####"
    if data['issue']['key'] is not None:
        newJSONObject['JIRATicketNumber'] = data['issue']['key']

    else:
        newJSONObject['JIRATicketNumber'] = "Not Given In JIRA"

    return f"{newJSONObject}\n"
