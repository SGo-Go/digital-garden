#!/usr/bin/python3

"""Customization for the devcontainer."""

import os

def get_workspace_root() -> str:
    """Get the real path to the project clone root folder."""
    return os.path.dirname(os.path.realpath(os.path.dirname(os.path.abspath(__file__))))

def check_config_files() -> str:
    return """
        touch ${HOME}/.gitconfig
        touch ${HOME}/.git-credentials
        touch ${HOME}/.Xauthority
        mkdir -p /tmp/.X11-unix
        mkdir -p ~/.ssh"""

def customize_docker(base_os="slim") -> None:
    """Add user docker compose to the devcontainer."""

    workspace_root = get_workspace_root()

    docker_compose_user_file = os.path.join(get_workspace_root(), ".devcontainer", "docker-compose.user.yml")
    if os.path.exists(docker_compose_user_file):
        print(f"`devcontainer` customization file {docker_compose_user_file} already exists.")
        return

    with open(os.path.join(workspace_root, ".python-version"), "r") as file_handle:
        python_version = file_handle.read().rstrip()

    with open(docker_compose_user_file, "w") as file_handle:
        file_handle.write(rf"""#yaml
# Generated devcontainer customization file
services:
  digital_garden:
    build:
      args:
        PYTHON_VERSION: {python_version}
        BASE_OS: {base_os}
    environment: []
""")

def main() -> None:
    customize_docker()

if __name__ == "__main__":
    main()
