# Openshifter
is an experimental design study to figure out how microservice-based applications can and should be migrated in various forms.

The implementation is based on OpenShift, hence the (slightly non-creative and trademark-offensive) name.

## Installation:
#### Prerequisites:
- python3
- pip3
- openssl

#### Setup:

- Run `install.sh`

(The certs generated are self signed so they have to be trusted manually the first time.)

## Usage:
- To automate the process of migration, you can specify information about your OpenShift instances in the `input.json` so you don't have to input them manually on every run.
- Launch the openshifter server (`openshifter.py`).
- Launch the client (`openshifterlient.py`) and follow the instructions. You will be asked to provide or select context information and the semantics of your migration (see notes)

## Notes:
- Purposeful insecure design during prototyping phase
- The only operation currently explicitly supported by the client is `testmove` which does the following:
  - export from source
  - delete on source
  - import to target
- Copy operations would ommit the deletion step and a real move operation would delete only after import has been completed successfully.
- Selecting anything other than `testmove` as the operation type will result in a copy operation. **This will most likely fail if source and target are the same instance.**

## Known Issues
- Minishift causes the python client to crash. Until this can be fixed use `testclient.sh` to test migrations to or from a minishift instance.
- Sometimes when migrating to the same instance as the source, the user has to trigger the build manually from the dashboard due to a permission issue. This does not affect minishift.
