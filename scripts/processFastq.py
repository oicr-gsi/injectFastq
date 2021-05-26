import argparse
import gzip
import os
import subprocess
import sys

parser = argparse.ArgumentParser(prog='processFastq.py', description="A tool for fastq validation")

parser.add_argument('-f1', '--Fastq1', dest='fastq1', help='Path to Fastq1', required=True)
parser.add_argument('-f2', '--Fastq2', dest='fastq2', help='Path to Fastq2', required=True)
parser.add_argument('-r', '--Run', dest='run', help='Run name', required=True)
parser.add_argument('-s', '--Sample', dest='sample', help='Sample name', required=True)

args = parser.parse_args()


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


checkR1R2(args.fastq1, args.fastq2, args.sample)
