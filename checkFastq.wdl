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
        name: "python3/3.6",
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
    String modules = "python/3.6"
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
  }

  command <<<
   python3<<CODE
   import gzip
   import os
   import subprocess
   import sys 
   def readfile(fastq):
       fastqfile = gzip.open(fastq, "rb")
       contents = fastqfile.read()
       return contents


   def checkR1R2(r1, r2, sample):
       """ extract the headers and check if they are the same for R1 and R2 """
       cmd = 'zcat ' + r1 + ' | paste - - - - | cut -f 1 -d " " ' + '> headerR1'
       os.system(cmd)
       cmd = 'zcat ' + r2 + ' | paste - - - - | cut -f 1 -d " " ' + '> headerR2'
       os.system(cmd)

       proc = subprocess.check_output('md5sum {0}'.format('headerR1'), shell=True).decode('utf-8').rstrip().split()[0]
       proc2 = subprocess.check_output('md5sum {0}'.format('headerR2'), shell=True).decode('utf-8').rstrip().split()[0]

       countR1 = subprocess.check_output('cat headerR1 | wc -l', shell=True).decode('utf-8').rstrip().split()[0]
       countR2 = subprocess.check_output('cat headerR2 | wc -l', shell=True).decode('utf-8').rstrip().split()[0]

       if (countR1 != countR2):
           die('Read count mismatch!')

       """ if headers are different, sort R1 and R2 """
       if (proc2 != proc):
           sortfile(r1)
           sortfile(r2)
       else:
           cmd = 'cp ' + r1 + ' ' + sample + '_R1.fastq.gz'
           os.system(cmd)
           cmd = 'cp ' + r2 + ' ' + sample + '_R2.fastq.gz'
           os.system(cmd)


   def sortfile(fastq):
       out = os.path.basename(fastq)
       cmd = 'zcat ' + fastq + ' | paste - - - - | sort -k1,1 |tr ' + '"\\t"' + ' "\\n"' + ' | gzip >' + out
       print(cmd)
       os.system(cmd)

   def die(msg):
       print(msg)
       sys.exit(1)


   checkR1R2("~{pFastqR1}", "~{pFastqR2}", "~{sample}")
   CODE
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
