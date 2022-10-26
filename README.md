# Python Server

## Development Environment

The project requires the following dependencies.

1. Install `curl`:
    - `sudo apt install curl`
2. Install `python3` and `python3-pip`:
    - `sudo apt install python3 python3-pip`
3. Install pip packages `flask`, `flask-ngrok`, `slackclient` and `slackeventsapi`:
    - `pip3 install flask flask-ngrok slackclient slackeventsapi`
        - There may be an issue where pip3 will complain that the install location of python modules is not in the path. To solve this problem run the command `PATH=$PATH:location/to/local/modules`

Clone the repo to your local machine.

### TODO: Testing
## Testing

1. To test the flask server.py, open a new terminal and type:
    - `flask --app server.py run -p 8088`
2. In another terminal:
    - `./run_webhook_test`
