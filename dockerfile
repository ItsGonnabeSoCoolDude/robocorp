# Multi-stage build to support multiple Python versions
ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Conda for environment management
FROM base AS conda
RUN pip install --no-cache-dir conda && \
    conda config --add channels conda-forge

# Final stage
FROM conda AS final

# Copy configuration files
COPY conda.yml robot.yaml ./
COPY tasks.py ./

# Install dependencies from conda.yml
RUN conda env create -f conda.yml && \
    conda clean --all -f -y

# Install Playwright browsers
RUN python -m playwright install chromium && \
    python -m playwright install-deps

# Set environment variables
ENV PATH="/opt/conda/envs/env/bin:$PATH"
ENV PYTHONPATH="/app:."

# Create output directory
RUN mkdir -p /app/output

# Set entrypoint
ENTRYPOINT ["python", "-m", "robocorp.tasks", "run", "tasks.py"]