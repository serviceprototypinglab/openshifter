import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

v1_services = dyn_client.resources.get(api_version='v1', kind='ServiceList')




resp = v1_services.get(namespace='zhaw-devtest')

# resp is a ResourceInstance object
print(resp)
