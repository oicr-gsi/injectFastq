version 1.0

workflow injectFastq {
input {
    File fastqR1
    File fastqR2
    String sampleName
    String runName
  }

  parameter_meta {
    fastqR1: "Fastq R1"
    fastqR2: "Fastq R2"
    sampleName: "Sample Name"
    runName: "run name of the fastq files"
  }

  meta {
    author: "Yogi Sundaravadanam"
    email: "ysundaravadanam@oicr.on.ca"
    description: "A pipeline that will inject Fastq files "
    dependencies: [
      {
        name: "python3/3.6",
        url: "https://www.python.org/downloads/release/python-360/"
      }
    ]
    
    output_meta: {
      outFastqR1: "sorted fastq1",
      outFastqR2: "sorted fastq2 ",
    }
  }

  call processFastq {
    input:
      pFastqR1 = fastqR1,
      pFastqR2 = fastqR2,
      sample = sampleName,
      run = runName
  }

  output {
    File outFastqR1 = processFastq.oFastqR1
    File outFastqR2 = processFastq.oFastqR2
  }
}
  
task processFastq {
  input {
    String modules = "python/3.6"
    File pFastqR1
    File pFastqR2
    String run
    String sample
    Int timeout = 72
    Int jobMemory = 24
    Int mem = 48
    Int overhead = 6
    Int cores = 1
  }

  parameter_meta {
    pFastqR1: "R1"
    pFastqR2: "R2"
    run: "Run name for the fastqs"
    sample: "Sample prefix "
    mem: "Memory allocated for alignment task"
    timeout: "Timeout in hours for this task"
    jobMemory: "Java memory for Picard"
    cores: "The number of cores to allocate to the job."
    modules: "Names and versions of modules needed for variant calling"
  }

  command <<<
  set -euo pipefail

  #Call python script - this needs to be in modulator evenutually
  python3 /.mounts/labs/gsiprojects/gsi/injection/processFastq.py -f1 ~{pFastqR1} -f2 ~{pFastqR2} -r ~{run} -s ~{sample}
  
  >>>

  runtime {
    memory: "~{mem} GB"
    modules: "~{modules}"
    timeout: "~{timeout}"
    cpu: "~{cores}"
  }

  output {
    File oFastqR1 = "~{sample}_R1.fastq.gz"
    File oFastqR2 = "~{sample}_R2.fastq.gz"
  }
}
