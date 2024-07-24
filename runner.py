import subprocess

# Python sunucusunu başlat
subprocess.Popen(["python", r"C:\Users\Bilge\Desktop\MechSoft_python_2_merged\MechSoftServer\run.py"], shell=True)

# Angular uygulamasını başlat
subprocess.Popen(r"cd .\MechSoftClient\ && ng serve", shell=True)
