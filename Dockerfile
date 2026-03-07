FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5002

ENV OTEL_PYTHON_LOG_CORRELATION=true
ENV OTEL_SERVICE_NAME=payment-service
ENV OTEL_EXPORTER_JAEGER_ENDPOINT=http://jaeger:14268/api/traces

CMD ["python", "app.py"]

