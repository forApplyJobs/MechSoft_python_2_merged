import subprocess
import os

try:
    file = open("seed.txt", 'r')
    print("seed working")
except IOError:
    file = open("seed.txt", 'w')
    os.system(r"python C:\Users\Bilge\Desktop\MechSoft_python_2_merged\MechSoftServer\seed.py")

# Python sunucusunu başlat
subprocess.Popen(["python", r"C:\Users\Bilge\Desktop\MechSoft_python_2_merged\MechSoftServer\run.py"], shell=True)

# Angular uygulamasını başlat
subprocess.Popen(r"cd .\MechSoftClient\ && ng serve", shell=True)
