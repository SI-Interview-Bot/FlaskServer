'''
Used to listen for webhooks from Jira on Orion to update InterviewBot.
'''

# Standard imports
import json

from os     import environ
from sys    import stdout
from typing import Tuple

# Non-standard imports
import requests

from flask import Flask, request

# REST API/End-points
RECEIVE_JIRA_JSON = "receive-JIRA-JSON"
ISSUE_UPDATE      = "issue-update"

app = Flask(__name__)

# Get IP and PORT of Slack Bot from environmental variables
try:
    DESTINATION = environ['SLACKBOT_IP_PORT']
except:
    DESTINATION = f"http://localhost:5000" # Default IP and PORT
finally:
    stdout.write(f"[i] Sending POST requests to {DESTINATION}\n")

def extract_interview_date_time_data(ret_json: dict, incoming_json: dict) -> Tuple[str, str]:
    '''
    NOTE: If the date and time are being entered in JIRA and server.py is
    producing a JSON object without that data, it could be formatted differently.
    server.py is expecting the value of this field to be delimited by a "T". Check if
    the date time format has changed in the JSON produced by JIRA's webhook and update
    how we parse that here.

    Expected format: "customfield_10003": "2022-10-07T19:30:00.000-0400"
    '''
    try:
        if incoming_json['issue']['fields']['customfield_10003'] is not None:
            ret_json['dateTime'] = incoming_json['issue']['fields']['customfield_10003']
            date = ret_json['dateTime'].split('T')[0]
            time = ret_json['dateTime'].split('T')[1].split('.')[0]
        else:
            ret_json['dateTime'] = "NULL"
            date = "NULL"
            time = "NULL"
    except:
        ret_json['dateTime'] = "extract_interview_date_time_data exception"

    return (date, time,)

def extract_name_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    Expected format: "summary": "firstName lastName"
    '''
    try:
        if incoming_json['issue']['fields']['summary'].split(" ")[0] is not None:
            ret_json['name'] = incoming_json['issue']['fields']['summary'].split(" ")[0]
        else:
            ret_json['name'] = "NULL"
    except:
        ret_json['name'] = "extract_name_data exception"

def extract_interview_type_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    The type of interview: Phone, Face-to-Face, etc.
    Expected format: "field": "Type of Interview"
    '''
    try:
        if incoming_json['changelog']['items'][0]['field'] is not None:
            ret_json['interviewType'] = incoming_json['changelog']['items'][0]['field']
        else:
            ret_json['interviewType'] = "NULL"
    except:
        ret_json['interviewType'] = "extract_interview_type_data exception"

def extract_jira_ticket_data(ret_json: dict, incoming_json: dict) -> None:
    '''
    Expected format: "key": "CT-####"
    '''
    try:
        if incoming_json['issue']['key'] is not None:
            ret_json['JIRATicketNumber'] = incoming_json['issue']['key']
        else:
            ret_json['JIRATicketNumber'] = "NULL"
    except:
        ret_json['JIRATicketNumber'] = "extract_jira_ticket_data exception"

def receive_data() -> dict:
    '''
    Receives and parses the JSON object into a dict()
    '''
    incoming_data = request.get_data()
    return json.loads(incoming_data)

@app.route(f'/{ISSUE_UPDATE}', methods=['POST'])
def parse_data() -> str:
    '''
    parse_data           - Takes a JSON Object from a JIRA webhook and parses information to
                           build another JSON Object in response.
    IN:  HTTP POST       - Handled by Flask
    OUT: ret_json_object - The JSON Object built with JIRA's JSON Object. We parse it here with
                           a specific format expected. Should the returned JSON Object start to
                           look weird, or just straight up useless, it could be that JIRA's
                           JSON Object has changed its formatting in such a way that we can no
                           longer parse it.
    '''
    ret_json_object = dict()
    incoming_json_object = receive_data()
    stdout.write(f"[+] Received /{ISSUE_UPDATE} POST.\n")

    extract_name_data(ret_json=ret_json_object,
                      incoming_json=incoming_json_object)

    extract_interview_type_data(ret_json=ret_json_object,
                                incoming_json=incoming_json_object)

    # Unused
    date, time = extract_interview_date_time_data(ret_json=ret_json_object,
                                                  incoming_json=incoming_json_object)

    extract_jira_ticket_data(ret_json=ret_json_object,
                             incoming_json=incoming_json_object)

    # Send a POST request to the bot's end-point with our clean JSON object
    try:
        response = requests.post(f'{DESTINATION}/{RECEIVE_JIRA_JSON}', json=ret_json_object)
        if "200" not in response.text:
            stdout.write(f"[X] Failed to send POST request. POST Response was: {response}\n")
            return f"[X] Failed to send POST request. POST Response was: {response}\n"
        else:
            stdout.write(f"[+] Sent POST request to {DESTINATION}/{RECEIVE_JIRA_JSON}\n")
            return f"[+] Sent POST request to {DESTINATION}/{RECEIVE_JIRA_JSON}\n"
    except Exception as error:
        stdout.write(f"[X] Failed to send POST request. Error:{error}\n")
        return f"[X] Failed to send POST request. Error:{error}\n"

    return f"{ret_json_object}\n"
