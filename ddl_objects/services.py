import cx_Oracle
from ddl_loader import db_conf


CURRENT_DB_CONNECTION: str = db_conf.DB_NAME
OWNER: str = db_conf.USER.upper()

_user: str = OWNER
_pwd: str = db_conf.PASSWORD
_service: str = db_conf.NAME

try:
    cx_Oracle.init_oracle_client(lib_dir=r"D:\src\instantclient_19_3")
except cx_Oracle.ProgrammingError:
    pass

_con = cx_Oracle.connect(_user, _pwd, _service)


def get_object_ddl_script_service(object_type: str, object_name: str) -> str:
    """Выгружает DDL скрипт объекта"""
    with _con.cursor() as cur:

        def output_type_handler(cursor, name, defaultType, size, precision, scale):
            """Настраиваем оракловый хэндлер для конвертации CLOB типа"""
            if defaultType == cx_Oracle.CLOB:
                return cursor.var(cx_Oracle.CLOB, arraysize=cursor.arraysize)

        _con.outputtypehandler = output_type_handler

        # Убираем размеры сегментов для таблиц
        cur.execute(
            """
            begin
              DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'STORAGE', false);
            end;
            """
        )
        # Стандартный АПИ для оракла пакет DBMS. Выгружаем DDL скрипт объекта
        cur.execute(
            """
            select DBMS_METADATA.GET_DDL(:object_type, :object_name, :owner) 
            from dual
            """, {'object_type': object_type.upper(), 'object_name': object_name.upper(), 'owner': _user.upper()}
        )

        (clob,) = cur.fetchone()

        return clob.read().replace('"', '')


def get_object_error_msg_service(object_type: str, object_name: str) -> cx_Oracle:
    """Выгружает текст ошибки компиляции объекта"""
    with _con.cursor() as cur:
        cur.execute(
            """
            select
                err.NAME
              , err.LINE as ERROR_LINE
              , err.TEXT as ERROR_MSG
              , substr(src.TEXT, err.POSITION) as ERROR_TEXT
            from ALL_OBJECTS obj
            join ALL_ERRORS err on obj.OBJECT_TYPE = err.TYPE and obj.OBJECT_NAME = err.NAME and err.OWNER = obj.OWNER
            join ALL_SOURCE src on err.OWNER = src.OWNER and src.TYPE = err.TYPE and err.LINE = src.LINE and err.NAME = src.NAME
            where 1 = 1
            and obj.OWNER = :owner
            and obj.STATUS = 'INVALID'
            and obj.OBJECT_TYPE = :object_type
            and obj.OBJECT_NAME = :object_name
            order by err.OWNER, err.TYPE, err.NAME, err.SEQUENCE
            """, {'object_type': object_type.upper(), 'object_name': object_name.upper(), 'owner': _user.upper()}
        )

        return cur.fetchall()
