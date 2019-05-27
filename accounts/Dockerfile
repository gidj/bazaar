FROM python:3

run apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY config.yml ./
COPY run.sh ./

COPY accounts ./accounts

RUN chmod +x ./run.sh

CMD ["./run.sh"]
