# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.13
FROM python:${PYTHON_VERSION}-slim as base

# ------ General Python & system setup

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser                   \
    --disabled-password       \
    --gecos ""                \
    --home "/nonexistent"     \
    --shell "/sbin/nologin"   \
    --no-create-home          \
    --uid "${UID}"            \
    appuser

# ------ Project modules deployment

# Set workdir to '/py-site' - it will be a root directory \
# for all custom Python modules from the project
WORKDIR /py-site

# Install project requirements using pip from modules requirements files:
# * db_utils_lib: lib/requirements.txt
# * db_utils: utils/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip                                                \
    --mount=type=bind,source=data_lib/requirements.txt,target=data_lib/requirements.txt       \
    --mount=type=bind,source=core/requirements.txt,target=web_manager_core/requirements.txt   \
    --mount=type=bind,source=app/requirements.txt,target=web_manager/requirements.txt         \
    python -m pip install -r data_lib/requirements.txt -r web_manager_core/requirements.txt -r web_manager/requirements.txt

# Copy the source code for all modules into the container:
# * db_utils_lib: lib/src -> py-site/db-utils-lib
# * db_utils_lib: utils/src -> py-site/db-utils
COPY app/src core/src data_lib/src ./

# Add 'py-site' directory to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/py-site/"

# ------ Final setup

# Change working directory to '.work' - it will be the main working catalog,
# run all following commands from there by default
WORKDIR /.work
