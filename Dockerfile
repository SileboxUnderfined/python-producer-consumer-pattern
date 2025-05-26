FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv --copies /opt/venv

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && /opt/venv/bin/pip uninstall -y pip setuptools wheel

FROM alpine:latest AS worker

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY --from=builder /usr/local/lib /usr/local/lib

COPY ./src/ ./

ENV PATH="/opt/venv/bin:$PATH"
ENV DEBUG="0"
ENV WAITRESS_HOST="0.0.0.0"
ENV WAITRESS_PORT="80"

EXPOSE 80

ENTRYPOINT ["python"]

CMD ["main.py"]