# -*- coding: utf-8
# potrebne kniznice. GLOB + OS na pouzivanie FILOV, RE na pracu s textom
# ConfigParser je treba na natiahnutie informacii z .ini suboru
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


def sensor_check(sensor_path):
    print('Nactitavam senzor')
# re.findall nachadza vsetky vyskyti pouziteho retazca
# - 28-* oznacuje directory a zaroven je aj IDckom cidla -
# v ceste nacitaych filoch do !LISTu! - [0] z toho robi string, pretoza alokuje len jednu hodnotu
    sensid = re.findall('(28-.*)/', sensor_path)[0]
# otvorenie filu, ktory je prave na rade
    file = open(sensor_path, "r")
# precitanie stavu cidla
    file_open = file.read()
#  TO DO  na tomto riadku, treba vychitat zapornu hodnotu! - zaporna hodnota vychytana pomoocou [\+\-]?
#  TO DO Este treba vychytat presnu 0. Cidlo vracia v pripade 0°C hodnotu 0 a nie 00000. - zrusene [0-9]{5} na odchytenie
#  piatich ciselnych znakov. Pouzite .* na nacitanie vsetkeho po kladnom/zapornom znamienku
    raw_temperature = re.findall('t=([\+\-]?.*)', file_open)[0]
# uzatvorenie subou, pretoze inak si ho python drzi otvoreny v procese a moze blokovat
    file.close()
# Osetrenie zapornej hodnoty, pretoze, ak ma zapornu hodnotu ma o poziciu viacej a udava to zle.
# Nutnost konvertovat na int(), pretoze findall vracia list, ktory konvertujem do string
# TO DO - dost krkolomne ist z listu do stringu a do integeru, treba pozriet, ako to odfiltrovat rovno do numerickej hodnoty
# TO DO - Zistit, ake hodnoty vychadzaju v pripade teplot medzi 0-10, ci su tiez 5 miestne, alebo nie.
    if int(raw_temperature) >0 and len(raw_temperature) == 5:
        temperature = raw_temperature[:2] + '.' + raw_temperature[2:]
    elif int(raw_temperature)<0 and len(raw_temperature) == 6:
        temperature = raw_temperature[:3] + '.' + raw_temperature[3:]
    elif int(raw_temperature) == 0:
        temperature = '00.000'
    else:
        # !!!!Neotestovane!!!!!
        raise ValueError('Chybni vstup na cidle')
    return sensid, temperature

def sensor_read(input_folder):
# loop cez vsetky najdene files ktore poskytuju data z cidiel
    sensor_list = os.path.join(input_folder, '28*/w1_slave')
    for sensor_file in sorted(glob.glob(sensor_list)):
        print(sensor_file)
        sensor_data = sensor_check(sensor_file)
        temperature = sensor_data[1]
        sensid = sensor_data[0]
# Vypis zisteni a insert
        print('Trosku iny pokus o vystup')
        print('Sensor ID: ' + sensid)
        print('Temperature : ' + temperature + ' °C')
        connection(sensid, temperature)


print('Vloz zdrojovy priecinok kde sa nachadzaju cidla - w1_bus_master: ')
# raw_input je pre python 2! pre python 3 treba pouzit input()
input_folder = input()
sensor_read(input_folder)


