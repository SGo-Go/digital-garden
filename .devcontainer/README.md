# VS Code devcontainer

## Build customizable base image locally

```sh
python3 .devcontainer/initialize.py
docker compose -f .devcontainer/docker-compose.base.yml -f .devcontainer/docker-compose.user.yml build
```
