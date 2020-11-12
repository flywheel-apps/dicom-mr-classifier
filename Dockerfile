FROM python:3.7-slim-stretch

#MAINTAINER Flywheel <support@flywheel.io>


RUN apt-get update && apt-get install -y git

COPY requirements.txt /opt
RUN pip install -r /opt/requirements.txt

WORKDIR /flywheel/v0

COPY manifest.json \
     run.py \
     classification_from_label.py \
     dicom_mr_classifier.py \
     ./

RUN chmod +x run.py
ENTRYPOINT ["/flywheel/v0/run.py"]
