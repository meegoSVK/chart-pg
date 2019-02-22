# -*- coding: utf-8
# potrebne kniznice. GLOB + OS na pouzivanie FILOV, RE na pracu s textom
import glob,os,re,psycopg2
from configparser import ConfigParser


# Okopcene z psycopg2 tutorialov
def config(filename='../ini/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

# okopcene z psycopg2 tutorialov
# Treba vymysliet nejaky bulk insert, pretoze stale otvaranie kurzorov a commity po jednom riadku su narocne
def connection(sensid, temperature):
    conn = None
    try:
        params = config()
        print('Connecting to Database')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('INSERTING DATA FROM SENSOR ' + sensid)
        cur.execute('INSERT INTO temperature (sensid, temperature) VALUES(%s,%s)', (sensid, temperature))
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



# loop cez vsetky najdene files ktore poskytuju data z cidiel
for sens_file in sorted(glob.glob('/sys/devices/w1_bus_master1/28*/w1_slave')):
    print("Nacitavam senzor: ")
# re.findall nachadza vsetky vyskyti pouziteho retazca
# - 28-* oznacuje directory a zaroven je aj IDckom cidla -
# v ceste nacitaych filoch do !LISTu! - [0] z toho robi string, pretoza alokuje len jednu hodnotu
    sensid = re.findall('(28-.*)/', sens_file)[0]
# otvorenie filu, ktory je prave na rade
    file = open(sens_file, "r")
# precitanie stavu cidla
    file_open = file.read()
# Precitanie piatich ciselnych znakov do premennej - znova pouzite [0] kvoli konverzii na string
#  TO DO  na tomto riadku, treba vychitat zapornu hodnotu!.
    raw_temperature = re.findall('t=([0-9]{5})', file_open)[0]
# uzatvorenie subou, pretoze inak si ho python drzi otvoreny v procese a moze blokovat
    file.close()
# Vypis zisteni - na poslednom riadku sa pouziva [:2] a [2:] na vlozenie bodky do printu
# - bude to nutne na integraciu do DB.
    temperature = raw_temperature[:2] + '.' + raw_temperature[2:]
    print(file_open)
    print('Trosku iny pokus o vystup')
    print('Sensor ID: ' + sensid)
    print('Temperature : ' + temperature + ' °C')
    connection(sensid, temperature)
