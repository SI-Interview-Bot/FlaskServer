'''
Used to listen for webhooks from Jira on Orion to update InterviewBot.
'''

# Standard imports
import json
from typing import Tuple

# Non-standard imports
from flask import Flask, request

app = Flask(__name__)


def extract_interview_date_time_data(ret_json: dict, incoming_json: dict) -> Tuple[str, str]:
    '''
    NOTE: If the date and time are being entered in JIRA and server.py is
    producing a JSON object without that data, it could be formatted differently.
    server.py is expecting the value of this field to be delimited by a "T". Check if
    the date time format has changed in the JSON produced by JIRA's webhook and update
    how we prase that here.

    Expected format: "customfield_10003": "2022-10-07T19:30:00.000-0400"
    '''
    try:
        ret_json['dateTime'] = incoming_json['issue']['fields']['customfield_10003']

        date = ret_json['dateTime'].split('T')[0]
        time = ret_json['dateTime'].split('T')[1].split('.')[0]
    except:
        ret_json['dateTime'] = "NULL"
        date = "NULL"
        time = "NULL"

    return (date, time,)


def extract_name_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    Expected format: "summary": "firstName lastName"
    '''
    if incoming_json['issue']['fields']['summary'].split(" ")[0] is not None:
        ret_json['name'] = incoming_json['issue']['fields']['summary'].split(" ")[0]
    else:
        ret_json['name'] = "NULL"


def recieve_data(incoming_json) -> dict:
    '''
    '''
    incoming_data = request.get_data()
    return json.loads(incoming_data)


def extract_interview_type_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    The type of interview: Phone, Face-to-Face, etc.
    Expected format: "field": "Type of Interview"
    '''
    if incoming_json['changelog']['items'][0]['field'] is not None:
        ret_json['interviewType'] = incoming_json['changelog']['items'][0]['field']
    else:
        ret_json['interviewType'] = "NULL"    


def extract_jira_ticket_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    Expected format: "key": "CT-####"
    '''
    if incoming_json['issue']['key'] is not None:
        ret_json['JIRATicketNumber'] = incoming_json['issue']['key']
    else:
        ret_json['JIRATicketNumber'] = "NULL"


@app.route('/issue-update', methods=['POST'])
def parse_data() -> str:
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

    ret_json_object = dict()
    incoming_json_object = recieve_data(request.get_data())

    extract_name_data(ret_json=ret_json_object,
                      incoming_json=incoming_json_object)

    extract_interview_type_data(ret_json=ret_json_object,
                                incoming_json=incoming_json_object)

    # Unused
    date, time = extract_interview_date_time_data(ret_json=ret_json_object,
                                                  incoming_json=incoming_json_object)

    extract_jira_ticket_data(ret_json=ret_json_object,
                             incoming_json=incoming_json_object)

    return f"{ret_json_object}\n"
