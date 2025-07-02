FROM python:3.12-alpine

WORKDIR /app

# Setup python env
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.6.1 /uv /uvx /bin/

# Copy package files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

CMD ["python", "server.py"]