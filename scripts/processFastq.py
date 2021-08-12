#!/usr/bin/env python3

import argparse
import os
import shutil
from subprocess import *
import sys

parser = argparse.ArgumentParser(prog='processFastq.py', description="A tool for fastq validation")

parser.add_argument('-f1', '--Fastq1', dest='fastq1', help='Path to Fastq1', required=True)
parser.add_argument('-f2', '--Fastq2', dest='fastq2', help='Path to Fastq2', required=True)
parser.add_argument('-s', '--Sample', dest='sample', help='Sample name', required=True)

args = parser.parse_args()


def getmd5sum(gzfile):
    psZcat = Popen(['zcat', gzfile], stdout=PIPE, shell=False)
    ps2 = Popen(['awk', '{if(NR%4==1){print $1}}'], stdout=PIPE, stdin=psZcat.stdout, shell=False)
    ps3 = run(['md5sum'], stdin=ps2.stdout, capture_output=True, text=True, shell=False)
    return ps3.stdout.strip().replace('-', '').strip()


def processHeader(gzfile):
    """ extract names of the reads in fastq file here, do count and md5sum. Return a tuple """
    psZcat = Popen(['zcat', gzfile], stdout=PIPE, shell=False)
    ps2 = Popen(['awk', 'NR%4==1'], stdout=PIPE, stdin=psZcat.stdout, shell=False)
    ps3 = run(['wc', '-l'], stdin=ps2.stdout, capture_output=True, text=True, shell=False)

    read_count = ps3.stdout.strip()
    md5sum = getmd5sum(gzfile) #ps3.stdout.encode('utf-8')

    if ps3.returncode != 0:
        die("Extracting reads failed for " + gzfile)

    return {'reads': int(read_count), 'md5sum': md5sum}


def checkR1R2(r1, r2, sample):
    """ extract the headers and check if they are the same for R1 and R2 """
    info1 = processHeader(r1)
    info2 = processHeader(r2)

    if info1['reads'] != info2['reads']:
        die('Read counts mismatch!')

    """ Define the files to save """
    save_R1 = r1
    save_R2 = r2

    """ if headers are different, sort R1 and R2 """
    if info1['md5sum'] != info2['md5sum']:
        print("Fixing files by sorting...")
        sortedR1 = sortfile(r1)
        sortedR2 = sortfile(r2)
        md_sorted1 = getmd5sum(sortedR1)
        md_sorted2 = getmd5sum(sortedR2)
        if md_sorted1 != md_sorted2:
            die("R1 and R2 Files do not match!")
        else:
            save_R1 = sortedR1
            save_R2 = sortedR2

    shutil.copy(save_R1, sample + '_R1.fastq.gz', follow_symlinks=True)
    shutil.copy(save_R2, sample + '_R2.fastq.gz', follow_symlinks=True)

def sortfile(gzfile):
    base = os.path.basename(gzfile)
    index_of_dot = base.index('.')
    out = base[:index_of_dot] + ".sorted.fastq.gz"
    """ we really need to use paste here, so we use os.system which is quite secure in this case """
    cmd = 'zcat ' + gzfile + ' | paste - - - - | sort -k1,1 | tr "\\t" "\\n" | gzip -c > ' + out
    os.system(cmd)
    return out


def die(msg):
    print(msg)
    sys.exit(1)


checkR1R2(args.fastq1, args.fastq2, args.sample)
