# Refactor testing
This directory is for development of the tools needed to refactor the export output to make it compatible with the import target.

Will be dropped once the tool is ready to integrate into openshifter.

## Goal:
- Decompress exported files
- Refactor template by:
  - Determining source namespace (can be determined during export step or provided as argument)
  - Replace with name of target namespace (provided as argument)
  - Remove "host:" fields from template
- Compress files ready to be imported to target
