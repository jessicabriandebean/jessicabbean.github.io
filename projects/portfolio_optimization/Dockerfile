FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen

COPY .. .

EXPOSE 8501

CMD ["/app/.venv/bin/streamlit", "run", "app/portfolio_streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]