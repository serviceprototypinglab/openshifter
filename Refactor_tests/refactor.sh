#Extract the exported template
rm -rf importprep; rm import.tgz
mkdir importprep; tar -xzvf _output.tgz -C importprep
cd importprep/*/templates

#Refactor the template
#We need to know the name of the source namespace
#and the name of the target namespace
python3 ../../../prepare.py $1 descriptor.json $2

#Prepare files for import and cleanup temp files
rm descriptor.json
mv new_descriptor.json descriptor.json
cd ../..
tar -zcvf ../import.tgz *; cd ..
rm -rf importprep
