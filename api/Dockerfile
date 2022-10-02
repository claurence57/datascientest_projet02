FROM ubuntu:20.04

ADD files/requirements.txt /datascientest/
ADD files/main.py /datascientest/
ADD files/model_final_test.joblib /datascientest/
ADD files/tfidf_vectorizer.joblib /datascientest/

RUN apt update -y
RUN apt upgrade -y
RUN apt autoremove -y

RUN apt install python3-pip -y
RUN pip install -r /datascientest/requirements.txt

EXPOSE 8000

WORKDIR /datascientest

CMD uvicorn main:server --host 0.0.0.0

