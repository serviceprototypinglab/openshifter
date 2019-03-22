# Openshifter
is an experimental design study to figure out how microservice-based applications can and should be migrated in various forms.

The implementation is based on OpenShift, hence the (slightly non-creative and trademark-offensive) name.

## Installation:
- Install requirements:
```
pip install -r requirements.txt
```

## Usage:
- Launch the openshifter server (`openshifter.py`).
- Launch the client (`openshifterlient.py`) and follow the instructions. You will be asked to provide:
  - Source context
  - Source namespace
  - Source username and password
  - Same thing for target
  - The type of operation to perform (See notes)

## Notes:
- Purposeful insecure design during prototyping phase
- The only operation currently explicitly supported by the client is `testmove` which does the following:
  - export from source
  - delete on source
  - import to target
- Copy operations would ommit the deletion step and a real move operation would delete only after import has been completed successfully.
- Writing anything other than `testmove` as the operation type will result in a copy operation. This will most likely fail if source and target are the same instance.
- Minishift causes the python client to crash. Use `testclient.sh` to test migrations to or from a minishift instance.
