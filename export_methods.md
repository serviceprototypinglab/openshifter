# Comparison of export methods

Comparison of the different methods available for exporting from a cluster offered by either kubectl or oc.

## Methods tested:
oc get all --export -o json  
oc get all -o json  
kubectl get all --export -o json  
kubectl get all -o -json

## Expected outcome:
Using oc or kubectl should not matter since oc is an extension of kubectl.  
The --export flag should filter out cluster-specific information.

## Results:
All 4 commands yielded identical json files.

## Testing method:
Ran all 4 commands on the same context. The test was made on a sample Django-Psql-Persistent deployment that was scaled and updated prior to export.
Redirected output to json files.  
File comparison between the 4 output files (using Atom editor's Compare Files package).

## Versions tested:
oc v3.11.0+0cbc58b  
kubectl v1.13.4

## Consequence:
We have to manually strip some fields and refactor some others for import across different clusters and namespaces.

## Solution:
Implemented the refactor script on the client side. This was done to avoid significantly altering the server design since we need to know both the source and target context to refactor.
