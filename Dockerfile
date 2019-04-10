FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN chmod +x ./oc
RUN mv ./oc /usr/local/bin
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "openshifter.py" ]
