#curl http://localhost:8080/contexts
#curl http://localhost:8080/spaces
#curl http://localhost:8080/descriptor/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1
#curl http://localhost:8080/volumes/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1
#curl http://localhost:8080/export/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1

alias oc='oc'

rm -rf _*

curl http://localhost:8080/export/192.168.99.100:8443/console/project/myproject/developer/developer > _output
base64 -d < _output > _output.tgz

oc delete all --all
while true; do echo -n .; status=`oc get all 2>&1`; if [ "$status" = "No resources found." ]; then break; fi; sleep 1; done; echo

curl -X POST --data-urlencode @_output.tgz http://localhost:8080/import/192.168.99.100:8443/console/project/myproject/developer/developer

#curl -X POST --data-urlencode @requirements.txt http://localhost:8080/import/console.appuio.ch:8443/appuio-demo3922/demo3922@appuio.ch/BgG3Ks%o2
#curl -X POST --data-urlencode @_randominput.txt http://localhost:8080/import/console.appuio.ch:8443/appuio-demo3922/demo3922@appuio.ch/BgG3Ks%o2

# TODOs:
# - security
# - large file support
