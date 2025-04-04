# Multi-stage build for easy version switching
ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim AS base

# Set working directory
WORKDIR /workspaces/${localWorkspaceFolderBasename}

# Install system dependencies with caching
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a cache directory for apt (optional, for local testing)
RUN mkdir -p /var/cache/apt && \
    chmod -R 777 /var/cache/apt

# Install Robocorp Command Line (rcc) with volume-based caching
RUN mkdir -p /usr/local/robocorp/bin && \
    chmod -R 777 /usr/local/robocorp
RUN if [ ! -f /usr/local/robocorp/bin/rcc ]; then \
    curl -o rcc https://downloads.robocorp.com/rcc/releases/latest/linux64/rcc && \
    chmod +x rcc && \
    mv rcc /usr/local/robocorp/bin/ && \
    # Create directory for rcc's own cache
    mkdir -p /home/.robocorp && \
    chmod -R 777 /home/.robocorp; \
    fi

# Add rcc to PATH
ENV PATH="/usr/local/robocorp/bin:$PATH"

# Install Miniconda with volume-based caching
FROM base AS conda
# Miniconda will be mounted from the conda-cache volume, so only install if missing
RUN if [ ! -d /opt/conda ]; then \
    curl -sLo miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda config --add channels conda-forge && \
    /opt/conda/bin/conda clean -a -y; \
    fi

# Final stage
FROM conda AS final

# Copy configuration files from the parent directory
COPY ../conda.yml ../robot.yaml ./
COPY ../tasks.py ./

# Create Conda environment with volume-based caching
RUN if [ ! -d /opt/conda/envs/env ]; then \
    /opt/conda/bin/conda env create -f conda.yml -p /opt/conda/envs/env && \
    /opt/conda/bin/conda clean --all -f -y; \
    fi

# Install Playwright browsers with volume-based caching
RUN mkdir -p /root/.cache/ms-playwright && \
    chmod -R 777 /root/.cache/ms-playwright
RUN if [ ! -d /root/.cache/ms-playwright/chromium ]; then \
    /opt/conda/envs/env/bin/python -m playwright install chromium && \
    /opt/conda/envs/env/bin/python -m playwright install-deps; \
    fi

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