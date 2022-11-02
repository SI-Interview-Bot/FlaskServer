# Python Server

## Development Environment

We will use Docker Engine to manage all dependencies for development and deployment of our solution.

1. Install `git`:
    - Follow: https://www.digitalocean.com/community/tutorials/how-to-install-git-on-centos-7
3. Install `Docker`:
    - Follow: https://docs.docker.com/engine/install/centos/
4. Install `docker-compose`
    - Follow: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

Clone the repo to your local machine.
`git clone <xxx>`

## Generate Docker image
1. `docker build -t json_cleaner_image:latest .`

## Testing

1. Update docker-compose.yaml file to use the bot's IP and PORT after bot is deployed.
2. In a terminal:
    - `docker-compose up`
3. In another terminal, if the process started by the last command was not detached:
    - `./run_webhook_test`

## Deployment

If you are deploying on a machine using a proxy server, configure Docker to use the proxy server:
https://docs.docker.com/config/daemon/systemd/

To build the Docker image use a similar command:
`docker build  --no-cache --build-arg HTTP_PROXY=http://xx.xx.xx.xx:xx --build-arg HTTPS_PROXY=http://xx.xx.xx.xx:xx -t json_cleaner_image .`
This is required so that once `pip` is installed and begins downloading the required modules in `requirements.txt` pip can also use the proxy server.
