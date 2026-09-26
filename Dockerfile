FROM python:3.13-slim
# Sicherheitsstand des Basis-Image nachziehen. Ein Upstream-Image friert die Paketstaende
# vom Tag seines Baus ein, Debian-security ist regelmaessig weiter, und ein `--pull` holt
# nur ein neueres Bild derselben Verspaetung: gemessen am 2026-09-13 trug das aktuelle
# python:3.13-slim aus der Registry dieselben drei perl-CVEs wie das monatealte lokale.
# `upgrade`, nicht `dist-upgrade`: letzteres darf Pakete entfernen, um Konflikte zu loesen.
RUN apt-get update \
 && apt-get -y upgrade \
 && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN pip install paho-mqtt==2.1.0 structlog==24.4.0
COPY tap.py .

RUN useradd -m -u 1000 tap && chown -R tap:tap /app
USER tap

CMD ["python", "-u", "tap.py"]
