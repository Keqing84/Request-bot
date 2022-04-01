FROM python:3.9.7-slim-buster

WORKDIR .
COPY . .

RUN apt-get update && apt upgrade -y \
  && apt-get -y install git

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]
