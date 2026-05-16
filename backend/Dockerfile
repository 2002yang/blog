FROM python:3.12-slim

WORKDIR /app

# psycopg2-binary 等依赖均有预编译 wheel，无需安装 gcc/libpq-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
