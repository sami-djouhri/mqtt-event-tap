FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN pip install paho-mqtt==2.1.0 structlog==24.4.0
COPY tap.py .

RUN useradd -m -u 1000 tap && chown -R tap:tap /app
USER tap

CMD ["python", "-u", "tap.py"]
