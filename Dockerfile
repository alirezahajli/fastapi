FROM python:3.9-slim-buster


RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean


RUN apt update && apt install -y gdebi-core libnss3 libgconf-2-4
ADD google-chrome-stable_current_amd64.deb .
RUN gdebi -n google-chrome-stable_current_amd64.deb

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD chromedriver .
RUN chmod +x chromedriver
COPY main.py .
COPY database.py .
COPY googlesearch.py .
COPY schemas.py .

EXPOSE 8000

# CMD ["uvicorn","main:app","--host=0.0.0.0","--reload"]
