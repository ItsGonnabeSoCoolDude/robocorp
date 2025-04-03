# Multi-stage build to support multiple Python versions
ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim AS base

# Set working directory
WORKDIR /workspaces/${localWorkspaceFolderBasename}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
FROM base AS conda
RUN curl -sLo miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda config --add channels conda-forge && \
    /opt/conda/bin/conda clean -a -y

# Final stage
FROM conda AS final

# Copy configuration files
COPY conda.yml robot.yaml ./
COPY tasks.py ./

# Create Conda environment from conda.yml
RUN /opt/conda/bin/conda env create -f conda.yml -p /opt/conda/envs/env && \
    /opt/conda/bin/conda clean --all -f -y

# Install Playwright browsers
RUN /opt/conda/envs/env/bin/python -m playwright install chromium && \
    /opt/conda/envs/env/bin/python -m playwright install-deps

# Set environment variables
ENV PATH="/opt/conda/envs/env/bin:$PATH"
ENV PYTHONPATH="/workspaces/${localWorkspaceFolderBasename}:."

# Create output directory
RUN mkdir -p /workspaces/${localWorkspaceFolderBasename}/output

# Install VS Code user setup
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

USER $USERNAME