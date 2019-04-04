# Evaluation
For evaluation of the current version of the tool, an experiment was carried out to measure its performance in various migration scenarios.
## Setup
For the purposes of the measurement, the sample Django app was used as the migrated application.  
The migration scenarios tested were:
- APPUiO -> APPUiO
- minishift -> minishift
- minishift -> APPUiO
- APPUiO -> minishift  

Each migration was ran 10 times to measure an average and standard deviation.

## Results

|||                             Scenarios                                             |||
|:-------------------------------------------------------------------------------------:|
|       |APPUiO -> APPUiO|minishift -> minishift|minishift -> APPUiO|APPUiO -> minishift|
|Average|27.969          |21.985                |21.551             |25.04              |
|SD     |6.833           |3.748                 |5.649              |3.65               |

## Observations
- The determining factor for the measured times was waiting for the server's response for `oc delete`. This can easily be observed by examining how close the averages are for migrations with the same source (since the source is running the deletion).
- In a production scenario, deletion will happen after migration is complete, and as such can be relegated to a separate process. This will increase performance significantly.
- For reference, (though no separate repeated experiment has been made) here are some sample measurements for factors that affect performance, but cannot be controlled by the tool.

|reference times|
|:---:|
|Minishift deletion*|~5-30 seconds|
|Minishift build|~30 seconds|
|APPUiO deletion*|~15-35 seconds|
|APPUiO build|~2 minutes|
|migration with no deletion|~5 seconds|  

*Deletion times vary wildly between runs due to waiting for a response from the server.


## Limitations
The times listed do not include the time to build the docker image on the target, as the build could not be triggered automatically for the homogeneous scenarios.
