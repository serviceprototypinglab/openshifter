#!/usr/bin/env bash
#Export from minishift:
curl -k https://localhost:8443/export/192.168.99.102:8443/myproject/developer/asdf > _output
#Export from APPUiO:
#curl -k https://localhost:8443/export/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur > _output
#Package export output for input
base64 -d < _output > _output.tgz
#Delete from minishift
#curl -k https://localhost:8443/delete/192.168.99.101:8443/myproject/developer/asdf
#Delete from APPUiO
#curl -k https://localhost:8443/delete/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur
#Import to minishift:
#curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/192.168.99.101:8443/myproject/developer/asdf
#Import to APPUiO:
curl -k -X POST --data-urlencode @_output.tgz https://localhost:8443/import/console.appuio.ch:443/zhaw-devtest/zhaw-pgkikopoulos1/6693Tak!27414!3ur
