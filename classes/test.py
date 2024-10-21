import subprocess

temp = subprocess.check_output(['/usr/bin/vcgencmd', 'measure_temp']).decode('UTF-8')
print(temp)
