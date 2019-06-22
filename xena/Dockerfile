# DOCKERFILE INSTALLATION FOR XENA
FROM ubuntu:latest
MAINTAINER Surya Saini "sainisurya.1@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /xena
WORKDIR /xena
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["views.py"]