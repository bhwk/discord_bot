FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3-pip
RUN apt-get install openjdk-11-jdk
WORKDIR /discord_bot
COPY requirements.txt /discord_bot/
RUN pip install -r requirements.txt
COPY . /discord_bot
CMD python main.py

