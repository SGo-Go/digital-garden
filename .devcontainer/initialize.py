#!/usr/bin/python3

"""Customization for the devcontainer."""

import os

def get_workspace_root() -> str:
    """Get the real path to the project clone root folder."""
    return os.path.dirname(os.path.realpath(os.path.dirname(os.path.abspath(__file__))))

def to_docker_path(path: str) -> str:
    """Normalize the path to use with docker compose"""

    if os.name == 'posix': # no need to convert
        return path
    elif os.name != 'nt' or sys.platform == 'win32': # windows -> do conversion
        posix_path = os.path.normpath(path).replace("\\", "/")
        drive, tail = os.path.splitdrive(posix_path)
        drive = drive[0].lower()
        return f"/{drive}{tail}"
    else: # unknown -> return original path
        print("WARNING: unknown OS, path adoption is not applicable")
        return path

def check_config_files() -> str:
    return """
        touch ${HOME}/.gitconfig
        touch ${HOME}/.git-credentials
        touch ${HOME}/.Xauthority
        mkdir -p /tmp/.X11-unix
        mkdir -p ~/.ssh"""

def customize_docker(base_os="slim", host_data_path=os.path.join(os.path.expanduser("~"), "data")) -> None:
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
      volumes:
      - {to_docker_path(host_data_path)}:/data
    environment: []
""")

def main() -> None:
    customize_docker()

if __name__ == "__main__":
    main()
