# Define base image
ARG PYTHON_VERSION=3.13.3
ARG BASE_OS="slim-bookworm"
FROM python:$PYTHON_VERSION-$BASE_OS

ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USERNAME
ARG DOCKER_GID=999

ARG http_proxy
ARG https_proxy

# Note: ARG are set as ENV vars, but not persisted in the final image
ENV USERNAME=$USERNAME

USER root

COPY requirements.in ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Introduce non-root user as a sudoer
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --create-home --gid ${USER_GID} --uid ${USER_UID} ${USERNAME} \
    && usermod -aG sudo ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers \
    && mkdir -p /home/${USERNAME} \
    && chown -R ${USER_UID}:${USER_GID} /home/${USERNAME} \
    && mkdir /workspace && chown -R ${USER_UID}:${USER_GID} /workspace \
    && mkdir /data && chown -R ${USER_UID}:${USER_GID} /data

# End user setups
SHELL [ "/bin/bash", "-c" ]
ENV SHELL=/bin/bash
USER ${USERNAME}

WORKDIR /workspace
