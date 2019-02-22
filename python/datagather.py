import glob,os,re
for sens_file in sorted(glob.glob('/sys/devices/w1_bus_master1/28*/w1_slave')):
    print("Nacitavam senzor: ")
    sensid = re.findall('(28-.*)/', sens_file)[0]
    file = open(sens_file, "r")
    file_open = file.read()
    raw_temperature = re.findall('t=([0-9]{5})', file_open)[0]
    file.close()
    print(file_open)
    print('Trosku iny pokus o vystup')
    print('Sensor ID: ' + sensid)
    print('Temperature : ' + raw_temperature[:2] + '.' + raw_temperature[2:] + ' °C')