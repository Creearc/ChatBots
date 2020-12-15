FROM python:3.6.6-slim 

WORKDIR /home/students/stalknia/Papka

COPY requirements.txt ./

RUN pip install --upgrade pip -r requirements.txt; exit 0

COPY apps apps
COPY tests tests
COPY ask.py ex5.2_backend.py ex5.2_frontend.py  ./

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

