import os
import sys
import subprocess

main_path = os.getcwd()
print(main_path)

path = 'apps'

for f in os.listdir(path):
  os.chdir(main_path)
  p = '{}\\{}'.format(path, f)
  if os.path.isdir(p) and f[0] != '_':
    os.chdir('{}\\{}'.format(main_path, p))
    proc = 'python app_{}.py'.format(f)
    print(proc)
    theproc = subprocess.Popen(proc, shell = True)
    print('Started')

    
