FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

EXPOSE 8000

WORKDIR /workspace

COPY . /workspace/

ENV UV_PROJECT_ENVIRONMENT=/workspace/.venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

CMD ["uv", "run", "uvicorn", "mcp_tools.main:starlette_app", "--host", "0.0.0.0", "--port", "8000"]
