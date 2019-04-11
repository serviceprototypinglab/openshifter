FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
COPY . /app
WORKDIR /app
ADD https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz .
RUN tar -xzvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
RUN chmod +x openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc
RUN mv openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/bin
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "openshifter.py" ]
