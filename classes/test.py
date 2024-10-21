from subprocess import call

temp = call('/opt/vc/bin/vcgencmd measure_temp')
print(temp)