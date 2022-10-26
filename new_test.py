from http import client
import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
#client.chat_postMessage(channel='#interviewbot-test', text="Hello World!")

@slack_event_adapter.on('message')
def message(payLoad) -> None:
    channel_id = event.get('channel')

    if channel_id != "#interviewbot-test":
        return

    event = payLoad.get('event', {})

if __name__ == "__main__":
    app.run(debug=True, port=8088)