version 1.0

workflow checkFastq {
input {
    File fastqR1
    File fastqR2
    String sampleName
  }

  parameter_meta {
    fastqR1: "Fastq R1"
    fastqR2: "Fastq R2"
    sampleName: "Sample Name"
  }

  meta {
    author: "Yogi Sundaravadanam, Peter Ruzanov"
    email: "ysundaravadanam@oicr.on.ca, pruzanov@oicr.on.ca"
    description: "A workflow for checking Fastq files, checks if R1 and R2 reads match (same number) and sorts fastq files if needed"
    dependencies: [
      {
        name: "python3/3.7",
        url: "https://www.python.org/downloads/release/python-360/"
      }
    ]
    
    output_meta: {
      outFastqR1: "sorted fastq1",
      outFastqR2: "sorted fastq2 "
    }
  }

  call processFastq {
    input:
      pFastqR1 = fastqR1,
      pFastqR2 = fastqR2,
      sample = sampleName,
  }

  output {
    File outFastqR1 = processFastq.oFastqR1
    File outFastqR2 = processFastq.oFastqR2
  }
}
  
task processFastq {
  input {
    String modules = "python/3.7 checkfastq-scripts/1.0"
    String checkScript = "$CHECKFASTQ_SCRIPTS_ROOT/processFastq.py"
    File pFastqR1
    File pFastqR2
    String sample
    Int timeout = 72
    Int jobMemory = 24
  }

  parameter_meta {
    pFastqR1: "R1"
    pFastqR2: "R2"
    sample: "Sample prefix"
    timeout: "Timeout in hours for this task"
    jobMemory: "Java memory for Picard"
    modules: "Names and versions of modules needed for variant calling"
    checkScript: "check script path, may be a custom path (useful for developing)" 
  }

  command <<<
   python3 ~{checkScript} -f1 ~{pFastqR1} -f2 ~{pFastqR2} -s ~{sample}
  >>>
  
  runtime {
    memory:  "~{jobMemory} GB"
    modules: "~{modules}"
    timeout: "~{timeout}"
  }

  output {
    File oFastqR1 = "~{sample}_R1.fastq.gz"
    File oFastqR2 = "~{sample}_R2.fastq.gz"
  }
}
