FROM debian:latest
RUN apt update -y
RUN apt upgrade -y
RUN apt autoremove -y
RUN apt install -y python3 python3-pip 
RUN pip3 install requests

ADD files/content.py datascientest/content.py
ADD files/test_conn.py datascientest/test_conn.py

WORKDIR /datascientest

CMD python3 content.py
