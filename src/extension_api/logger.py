from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler, INFO
import datetime
from config import config
LOG_FILE_DIR = '{}/log_{}.txt'.format(config['log']['LOG_DIR'],datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))

import subprocess
subprocess.run("dir={}; [ ! -e $dir ] && mkdir -p $dir".format(config['log']['LOG_DIR']),shell=True)

def get_module_logger(modname):
    #show_config(config)
    logger = getLogger(modname)
    logger.setLevel(DEBUG)
    # formatter = Formatter("%(asctime)s\t:%(lineno)-4d:%(levelname)-8s:%(funcName)-22s:%(message)s")
    formatter = Formatter("%(asctime)s\t:%(filename)-20s %(lineno)-4d:%(levelname)-8s:%(funcName)-22s:%(message)s")
    sh = StreamHandler()
    logger.addHandler(sh)
    sh.setLevel(DEBUG)
    sh.setFormatter(formatter)

    fh = FileHandler(LOG_FILE_DIR)
    logger.addHandler(fh)
    fh.setFormatter(formatter)

    logger.propagate = False
    return logger