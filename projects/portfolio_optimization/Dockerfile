FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

# Copy environment definition
COPY envs/portfolio_optimization/pyproject.toml .
RUN uv sync --frozen

COPY envs/portfolio_optimization/src ./src
COPY envs/portfolio_optimization/app ./app

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/portfolio_streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]