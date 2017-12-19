import platform
import subprocess
from smb.SMBConnection import SMBConnection
user = 't-hayashi'
password = 'tomonori'
conn = SMBConnection(
    user,
    password,
    platform.uname().node,
    'yellow',
    domain='wsl',
    use_ntlm_v2=True
)
conn.connect('192.168.60.10', 139)
items = conn.listPath('PUBLIC', 'scansnap')
yellow_num = list(filter(lambda x: '.pdf' in x, [item.filename for item in items]))
db_num = []
with open('../src/main_api/yellow_filenames.csv') as f:
    for name in f:
        db_num.append(name[:-1])
with open('../src/main_api/yellow_filenames.csv', 'w') as f:
    for name in yellow_num:
        f.write(name + '\n')
