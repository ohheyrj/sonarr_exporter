FROM python:3.7.9-slim-buster

COPY sonarr_exporter/sonarr_exporter.py sonarr_exporter.py

RUN pip install prometheus_client urllib3

EXPOSE 9315

ENTRYPOINT [ "python3", "sonarr_exporter.py" ]