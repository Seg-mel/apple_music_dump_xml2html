FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1
ENV UV_VERSION=0.11.8
ENV USERNAME=amx2h_user
ENV HOME_PATH=/home/${USERNAME}
ENV APP_ROOT=${HOME_PATH}/project

# Install system requirements
RUN apk update
RUN apk add --no-cache build-base python3-dev

# Install Python dependencies
RUN pip install --upgrade pip && pip install uv==$UV_VERSION
ADD pyproject.toml /
RUN uv pip install --system --no-cache --group main

# Create and change user
RUN adduser ${USERNAME} -h ${HOME_PATH} -s /bin/bash -D
USER ${USERNAME}:${USERNAME}

# Set workdir
RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
