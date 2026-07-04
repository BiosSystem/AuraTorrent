FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

# Run as a non-root user
RUN useradd --create-home --uid 1000 aurabot \
    && chown -R aurabot:aurabot /app
USER aurabot

CMD ["python", "main.py"]
