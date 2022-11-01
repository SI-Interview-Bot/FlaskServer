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
