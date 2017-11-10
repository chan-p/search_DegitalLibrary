import os
import codecs

files = os.listdir('../src/ver1/dlPDF')
count = 0
with codecs.open('../src/ver1/PDF_list.txt', 'w', 'utf-8') as f:
    for name in files:
        if '.zip' in name:
            f.write(name[:-8])
            if count < len(files)-2:
                f.write('\n')
        count += 1

"""
import platform
from smb.SMBConnection import SMBConnection

conn = SMBConnection(
        'administrator',
        'jvb1l0Iwata',
        platform.uname().node,
        'yellow.wsl.mind.meiji.ac.jp',
        domain='',
        use_ntlm_v2=True)
conn.connect('yellow.wsl.mind.meiji.ac.jp', 139)
"""
