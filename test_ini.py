import configparser
import os
import TS_var
import pymysql
from TS_f import config

ini = config('config.ini')

ini.config_setup()