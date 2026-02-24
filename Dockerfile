FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install packages one by one to avoid timeout
RUN pip install --no-cache-dir fastapi>=0.115.0 uvicorn[standard]>=0.32.0
RUN pip install --no-cache-dir sqlalchemy>=2.0.36 psycopg2-binary>=2.9.10 psycopg[binary]>=3.2.3 pgvector>=0.3.5
RUN pip install --no-cache-dir pydantic>=2.10.0 pydantic-settings>=2.6.0 python-dotenv>=1.0.1 upstash-redis>=0.15.0
RUN pip install --no-cache-dir numpy>=2.1.0
RUN pip install --no-cache-dir --timeout=2000 torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir sentence-transformers>=3.3.0

COPY . .
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
