FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git python3-pip ffmpeg -y
RUN apt install -y tzdata
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN cd /
RUN git clone https://github.com/AsmSafone/MegaDL-Bot
RUN cd MegaDL-Bot
WORKDIR /MegaDL-Bot

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 main.py
