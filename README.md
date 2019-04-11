# Openshifter
is an experimental design study to figure out how microservice-based applications can and should be migrated in various forms.

The implementation is based on OpenShift, hence the (slightly non-creative and trademark-offensive) name.

## Installation:
#### Prerequisites (local install):
- python3
- pip3
- openssl

#### Prerequisites (Docker version):
- docker

#### Setup (local install):
- Clone this repo

- Run `install.sh`

(The certs generated are self signed so they have to be trusted manually the first time.)

#### Setup Docker version (very early prototype):
- Run the container (Same cert issue as above except you don't have to generate them):
```
docker run -d -p 8443:8443 panosece/openshifter:v7
```

## Usage :
(Omit step 2 if you are using the Docker container)
1. To automate the process of migration, you can specify information about your OpenShift instances in the `input.json` so you don't have to input them manually on every run.
2. Launch the openshifter server (`openshifter.py`).
3. Launch the client (`openshifterlient.py`) and follow the instructions. You will be asked to provide or select context information and the semantics of your migration (see notes)



## Notes:
Supported operations for the interactive client:
- **Move**: Useful for *in place* migrations (source and target are the same) where import would be impossible without deleting first.
  - Exports from source
  - Deletes from source
  - Imports to target
- **Ping-Pong**: Useful for *round-trip* (from source to target then back to source) or repeated migrations since in the end both instances have a copy of the application.
  - Exports from source
  - Deletes from target
  - Imports to target
- **Copy**: Useful for migrations where deletion should not be triggered automatically or at all.
  - Exports from source
  - Imports to target

It should also be noted that since openshifter is a RESTful service you can also send HTTP requests independently from the client.

## Known Issues
- Sometimes when migrating to the same instance as the source, the user has to trigger the build manually from the dashboard due to a permission issue.
- Due to minishift's security limitations, the server makes insecure requests to the clusters. Removing this vulnerability would make openshifter incompatible with minishift.
