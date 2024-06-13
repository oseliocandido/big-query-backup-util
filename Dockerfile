FROM python:3.12-slim

WORKDIR /app

COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python","./generate_ddl_files.py"]
