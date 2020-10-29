FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir mlflow psycopg2

CMD ["sh", "-c", "mlflow server --backend-store-uri $BACKEND_STORE_URI --host 0.0.0.0 --default-artifact-root $ARTEFACT_STORE_URI --port 5000"]