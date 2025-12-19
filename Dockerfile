FROM python:3.11-slim

ARG PROJECT_NAME
ENV PROJECT_NAME=${PROJECT_NAME}

WORKDIR /app

# Install UV
RUN pip install --no-cache-dir uv

# Copy project-specific dependency files
COPY envs/${PROJECT_NAME}/pyproject.toml .
COPY envs/${PROJECT_NAME}/uv.lock* ./

# Create virtual environment and install dependencies
RUN uv venv && \
    uv sync --frozen

# Copy project code
COPY projects/${PROJECT_NAME} ./code

EXPOSE 8501

# Run Streamlit (adjust path as needed per project)
CMD [".venv/bin/streamlit", "run", "code/app.py", "--server.port=8501", "--server.address=0.0.0.0"]