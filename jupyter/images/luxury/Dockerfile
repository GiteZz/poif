FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ENV MLFLOW_TRACKING_URI="http://mlflow.jhub.be/"
