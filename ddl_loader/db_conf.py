import os
import json
from enum import Enum


class DBName(Enum):
    DBGRIGOREV = 0
    DWH_PROD = 1
    DWH_DEV = 2


class DBSchema(Enum):
    DWH_ODS = 0
    DWH_TRN = 1
    DWH_DDS = 2
    DWH_DMA = 3
    DWH_STAGE = 4
    DWH_DMA_CALC = 5


class DBObjectType(Enum):
    TABLE = 0
    PACKAGE = 1
    PROCEDURE = 2
    FUNCTION = 3
    INDEX = 4
    SEQUENCE = 5
    TRIGGER = 6


path = os.environ.get('db_connects')
print(path)
# Устанавливаем базу для подключения (для вьюх будем брать отсюда).
# TODO нужо реализовать в виде роутера. Но надо подумать над реализацией
DB_NAME = DBName.DWH_DEV.name
NAME = None
USER = None
PASSWORD = None

with open(path) as file:
    data = json.load(file)
    NAME = data[DB_NAME]['NAME']
    USER = data[DB_NAME]['USER']
    PASSWORD = data[DB_NAME]['PASSWORD']
