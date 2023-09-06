FROM ubuntu:latest
RUN apt-get update
RUN apt install -y python3
RUN apt install -y python3-pip
WORKDIR /discord_bot
COPY requirements.txt /discord_bot/
RUN pip install -r requirements.txt
COPY . /discord_bot
CMD python3 main.py
