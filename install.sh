#!/usr/bin/env bash
pip3 install -r requirements.txt
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout domain_srv.key -out domain_srv.crt
