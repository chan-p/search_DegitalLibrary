import configparser

config = configparser.ConfigParser()

section1 = 'LOCALTEST'
config.add_section(section1)
config.set(section1, 'host', '0.0.0.0')
config.set(section1, 'port', '5000')

with open('setting.ini', 'w') as file:
    config.write(file)
