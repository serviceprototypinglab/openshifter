import urllib
import requests
# Testing client for debugging the import functionality

# Target configuration

endpoint = "http://0.0.0.0:8080"
url = "console.appuio.ch:443"
project = "zhaw-devtest"
user = "zhaw-pgkikopoulos1"
password = "6693Tak!27414!3ur"

# Import request Testing
with open('import.tgz', 'rb') as f:
    data = f.read()
data = urllib.parse.quote(data)
requests.post('{}/import/{}/{}/{}/{}'.format(endpoint, url, project, user, password), data=data)
