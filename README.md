# checkFastq

A workflow for checking Fastq files, checks if R1 and R2 reads match (same number) and sorts fastq files if needed

## Dependencies

* [python3 3.7](https://www.python.org/downloads/release/python-370/)


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


#### Optional task parameters:
Parameter|Value|Default|Description
---|---|---|---
`processFastq.modules`|String|"python/3.7"|Names and versions of modules needed for variant calling
`processFastq.timeout`|Int|72|Timeout in hours for this task
`processFastq.jobMemory`|Int|24|Java memory for Picard


### Outputs

Output | Type | Description
---|---|---
`outFastqR1`|File|sorted fastq1
`outFastqR2`|File|sorted fastq2 


## Commands
This section lists command(s) run by WORKFLOW workflow
 
* Running WORKFLOW
 
Workflow runs a custom python script which checks a pair of fastq files for consistency, i.e. 
that number of reads matches and files are similarly sorted.
 
see the source of checkFastq.py script for details
 
## Support

For support, please file an issue on the [Github project](https://github.com/oicr-gsi) or send an email to gsi@oicr.on.ca .

_Generated with generate-markdown-readme (https://github.com/oicr-gsi/gsi-wdl-tools/)_
