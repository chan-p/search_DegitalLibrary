import os
import sys
import zipfile
import codecs

files = os.listdir('../src/ver1/dlPDF')
count = 0

exists = []
with open('../src/ver1/PDF_list.txt') as f:
    for name in f:
        exists.append(name.replace('\n', '') + '.pdf')

import subprocess

for name in files:
    if '.pdf' in name and '.zip' not in name and name not in exists:
        subprocess.call(["zip", '--junk-paths', 'file', '../src/ver1/dlPDF/' + name, name, '../src/ver1/dlPDF/' + name])
        subprocess.call(["mv", 'file.zip', '../src/ver1/dlPDF/' + name + '.zip'])

files = os.listdir('../src/ver1/dlPDF')
count = 0
with codecs.open('../src/ver1/PDF_list.txt', 'w', 'utf-8') as f:
    for name in files:
        if '.zip' in name:
            f.write(name[:-8])
            if count < len(files)-2:
                f.write('\n')
        count += 1
