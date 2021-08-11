#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
import hashlib

parser = argparse.ArgumentParser(prog='processFastq.py', description="A tool for fastq validation")

parser.add_argument('-f1', '--Fastq1', dest='fastq1', help='Path to Fastq1', required=True)
parser.add_argument('-f2', '--Fastq2', dest='fastq2', help='Path to Fastq2', required=True)
parser.add_argument('-s', '--Sample', dest='sample', help='Sample name', required=True)

args = parser.parse_args()

def getMd5sum(file):
    """ calculate md5sum for a file and return it """
    a_file = open(file, "rb")
    md5_hash = hashlib.md5()
    content = a_file.read()
    md5_hash.update(content)
    return md5_hash.hexdigest()


def createHeader(gzfile, header):
    """ extract names of the reads in fastq file here """
    with open(header, 'w') as h:
        psZcat = subprocess.Popen(['zcat', gzfile], stdout=subprocess.PIPE, shell=False)
        ps2 = subprocess.Popen(['awk', 'NR%4==1'], stdout=subprocess.PIPE, stdin=psZcat.stdout, shell=False)
        ps3 = subprocess.Popen(['cut', '-f', '1', '-d', " "], stdin=ps2.stdout, stdout=h, shell=False)
    print(ps3.communicate()[0])
    if ps3.returncode != 0:
        die("Extracting reads failed for " + gzfile)


def checkR1R2(r1, r2, sample):
    """ extract the headers and check if they are the same for R1 and R2 """
    createHeader(r1, 'headerR1')
    createHeader(r2, 'headerR2')
    countR1 = 0
    countR2 = 0
    for _ in open('headerR1').readlines():
        countR1 += 1
    for _ in open('headerR2').readlines():
        countR2 += 1

    if countR1 != countR2:
        die('Read counts mismatch!')

    """ Define the files to save """
    save_R1 = r1
    save_R2 = r2

    """ if headers are different, sort R1 and R2 """
    if getMd5sum('headerR2') != getMd5sum('headerR1'):
        sortedR1 = sortfile(r1)
        sortedR2 = sortfile(r2)
        createHeader(sortedR1, 'headerR1_sorted')
        createHeader(sortedR2, 'headerR2_sorted')
        if getMd5sum('headerR2_sorted') != getMd5sum('headerR1_sorted'):
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
