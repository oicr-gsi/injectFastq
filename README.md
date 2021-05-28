# checkFastq

A workflow for checking Fastq files, checks if R1 and R2 reads match (same number) and sorts fastq files if needed

## Overview

## Dependencies

* [python3 3.6](https://www.python.org/downloads/release/python-360/)


## Usage

### Cromwell
```
java -jar cromwell.jar run checkFastq.wdl --inputs inputs.json
```

### Inputs

#### Required workflow parameters:
Parameter|Value|Description
---|---|---
`fastqR1`|File|Fastq R1
`fastqR2`|File|Fastq R2
`sampleName`|String|Sample Name


#### Optional workflow parameters:
Parameter|Value|Default|Description
---|---|---|---


#### Optional task parameters:
Parameter|Value|Default|Description
---|---|---|---
`processFastq.modules`|String|"python/3.6"|Names and versions of modules needed for variant calling
`processFastq.timeout`|Int|72|Timeout in hours for this task
`processFastq.jobMemory`|Int|24|Java memory for Picard


### Outputs

Output | Type | Description
---|---|---
`outFastqR1`|File|sorted fastq1
`outFastqR2`|File|sorted fastq2 


## Niassa + Cromwell

This WDL workflow is wrapped in a Niassa workflow (https://github.com/oicr-gsi/pipedev/tree/master/pipedev-niassa-cromwell-workflow) so that it can used with the Niassa metadata tracking system (https://github.com/oicr-gsi/niassa).

* Building
```
mvn clean install
```

* Testing
```
mvn clean verify \
-Djava_opts="-Xmx1g -XX:+UseG1GC -XX:+UseStringDeduplication" \
-DrunTestThreads=2 \
-DskipITs=false \
-DskipRunITs=false \
-DworkingDirectory=/path/to/tmp/ \
-DschedulingHost=niassa_oozie_host \
-DwebserviceUrl=http://niassa-url:8080 \
-DwebserviceUser=niassa_user \
-DwebservicePassword=niassa_user_password \
-Dcromwell-host=http://cromwell-url:8000
```

## Support

For support, please file an issue on the [Github project](https://github.com/oicr-gsi) or send an email to gsi@oicr.on.ca .

_Generated with generate-markdown-readme (https://github.com/oicr-gsi/gsi-wdl-tools/)_
