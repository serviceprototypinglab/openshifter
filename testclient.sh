#!/usr/bin/env bash
#curl http://localhost:8080/contexts
#curl http://localhost:8080/spaces
#curl http://localhost:8080/descriptor/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1
#curl http://localhost:8080/volumes/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1
#curl http://localhost:8080/export/zhaw-hendu%2Fconsole-appuio-ch:8443%2Fzhaw-jspillner1/zhaw-test1
alias oc='oc'
rm -rf _*
#Export from minishift:
#curl -k https://localhost:8443/export/192.168.99.101:8443/myproject/developer/asdf > _output
#Export from APPUiO:
curl -k https://localhost:8443/export/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur > _output
base64 -d < _output > _output.tgz
#Delete from minishift
#curl -k https://localhost:8443/delete/192.168.99.101:8443/myproject/developer/asdf
#Delete from APPUiO
curl -k https://localhost:8443/delete/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur
#oc delete all --all
#while true; do echo -n .; status=`oc get all 2>&1`; if [ "$status" = "No resources found." ]; then break; fi; sleep 1; done; echo
#Import to minishift:
#python3 refactor.py zhaw-devtest myproject
curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/192.168.99.101:8443/myproject/developer/asdf
#Minishift to minishift:
#python3 refactor.py myproject myproject
#curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/192.168.99.101:8443/myproject/developer/asdf
#Import to APPUiO:
#python3 refactor.py myproject zhaw-devtest
#curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur
#APPUiO to APPUiO:
#python3 refactor.py zhaw-devtest zhaw-devtest
#curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur

#curl -k -X POST --data-urlencode @requirements.txt http://localhost:8080/import/console.appuio.ch:8443/appuio-demo3922/demo3922@appuio.ch/BgG3Ks%o2
#curl -k -X POST --data-urlencode @_randominput.txt http://localhost:8080/import/console.appuio.ch:8443/appuio-demo3922/demo3922@appuio.ch/BgG3Ks%o2

# TODOs:
# - security
# - large file support
#curl -X POST --data-urlencode @apptest.tgz http://localhost:8080/import/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur
