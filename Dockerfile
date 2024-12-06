# syntax=docker/dockerfile:1  # Enable Docker BuildKit features
# Keep this syntax directive! It's used to enable Docker BuildKit
# Tutorial:
# + https://nanmu.me/en/posts/2023/quick-dockerfile-for-python-poetry-projects/
# + https://blisscode.hashnode.dev/using-poetry-in-docker

########################################################
# PYTHON-BASE
# Sets up all our shared environment variables
########################################################

# Base image with Python
ARG PY_VERSION=3.12
FROM bitnami/python:${PY_VERSION} AS python-base

# Set the timezone to UTC
ARG TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG POETRY_VERSION=1.8.4

# Set environment variables for Python and Poetry
ENV \
    # Ensures Python output is sent directly to the terminal
    PYTHONUNBUFFERED=1 \
    # Disables unnecessary version check for pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # Sets a timeout for pip operations to prevent hangs
    PIP_DEFAULT_TIMEOUT=100 \
    # Specifies the Poetry version to use
    POETRY_VERSION=${POETRY_VERSION} \
    # Specifies the directory where Poetry is installed
    POETRY_HOME="/opt/poetry" \
    # Disables interactive prompts during Poetry installation
    POETRY_NO_INTERACTION=1 \
    # Instructs Poetry not to create virtual environments (since the container itself acts as an isolated environment)
    POETRY_VIRTUALENVS_CREATE=false \
    # Path to the virtual environment (created by Poetry)
    VIRTUAL_ENV="/venv"

# Prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN mkdir -p /usr/app
WORKDIR /usr/app

########################################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
########################################################
FROM python-base AS builder-base

# Set the default shell for subsequent RUN instructions in the Dockerfile to /bin/bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    # Install poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

# Copy only pyproject.toml and poetry.lock for efficient caching
COPY ./pyproject.toml poetry.lock ./

# install runtime deps to VIRTUAL_ENV
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --only main

WORKDIR /usr/app

# Copy project files
COPY . ./

########################################################
# DEVELOPMENT
# Image used during development / testing
########################################################

FROM builder-base AS development

# Set environment variables for Dev environment
ENV DEBUG=True

# Set the default shell for subsequent RUN instructions in the Dockerfile to /bin/bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install --no-install-recommends -y git zsh exa && \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh) --keep-zshrc" && \
    echo yes | bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"

RUN echo '\n# ZSH Plugins' >> ~/.zshrc && \
    echo "zinit light spaceship-prompt/spaceship-prompt" >> ~/.zshrc && \
    echo "zinit light zsh-users/zsh-syntax-highlighting" >> ~/.zshrc && \
    echo "zinit light zsh-users/zsh-autosuggestions" >> ~/.zshrc && \
    echo "zinit light zsh-users/zsh-completions" >> ~/.zshrc && \
    echo '\n# ZSH Snippet' >> ~/.zshrc && \
    echo "zinit snippet https://raw.githubusercontent.com/laragis/zsh-snippets/main/bash_aliases.sh" >> ~/.zshrc


WORKDIR /usr/app

# Quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root


########################################################
# PRODUCTION
# Final image used for runtime
########################################################
FROM python-base AS production

# Set environment variables for Prod environment
ENV DEBUG=False

# Copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /usr/app
COPY ./poetry.lock pyproject.toml ./
COPY . ./

USER 1001
