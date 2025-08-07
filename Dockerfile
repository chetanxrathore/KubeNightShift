FROM python:3.12-alpine

RUN pip install kubernetes

COPY scale_deployments.py /scale_deployments.py

CMD ["python", "/scale_deployments.py"]
