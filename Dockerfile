FROM python:3.12.4-slim as builder

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.12.4-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
