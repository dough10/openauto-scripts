from subprocess import call

temp = call(['/usr/bin/vcgencmd', 'measure_temp'])
print(temp)