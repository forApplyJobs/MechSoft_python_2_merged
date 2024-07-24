import subprocess
import os

try:
    file = open("seed.txt", 'r')
    print("seed working")
except IOError:
    file = open("seed.txt", 'w')
    os.system(r"python .\MechSoftServer\seed.py")

# Python sunucusunu başlat
subprocess.Popen(["python", r".\MechSoftServer\run.py"], shell=True)

# # Angular uygulamasını başlat
# subprocess.Popen(r"cd .\MechSoftClient\ && ng serve", shell=True)
