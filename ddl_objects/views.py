from django.shortcuts import render, HttpResponse
from django.views.generic import ListView

import cx_Oracle

from .models import BaseObject
from . import services
from . import utils
from ddl_loader import db_conf


class GetTablesView(ListView):
    """Возвращает наименование всех таблиц схемы"""

    model = BaseObject
    template_name = 'ddl_objects/data_table.html'
    queryset = BaseObject.all_tables.using(services.CURRENT_DB_CONNECTION).filter(owner=services.OWNER)
    paginate_by = 25


class GetProceduresView(ListView):
    """Возвращает наименование всех процедур схемы"""

    model = BaseObject
    template_name = 'ddl_objects/data_table.html'
    queryset = BaseObject.all_procedures.using(services.CURRENT_DB_CONNECTION).filter(owner=services.OWNER)


class GetFunctionsView(ListView):
    """Возвращает наименование всех функций схемы"""

    model = BaseObject
    template_name = 'ddl_objects/data_table.html'
    queryset = BaseObject.all_functions.using(services.CURRENT_DB_CONNECTION).filter(owner=services.OWNER)


class GetPackagesView(ListView):
    """Возвращает наименовение всех пакетов схемы"""

    model = BaseObject
    template_name = 'ddl_objects/data_table.html'
    queryset = BaseObject.all_packages.using(services.CURRENT_DB_CONNECTION).filter(owner=services.OWNER)


class GetSequencesView(ListView):
    """Возвращает наименование всех сиквенсов схемы"""

    model = BaseObject
    template_name = 'ddl_objects/data_table.html'
    queryset = BaseObject.all_sequences.using(services.CURRENT_DB_CONNECTION).filter(owner=services.OWNER)


def get_object_ddl_script(request, object_type: str, object_name: str):
    """Возвращает DDL скрипт объекта"""
    template_name = 'ddl_objects/data_detail.html'
    try:
        queryset = services.get_object_ddl_script_service(object_type, object_name)
        return render(request, template_name, {'object_list': queryset, 'is_error': 0, 'object_name': object_name})
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 31603:
            return render(request, template_name, {
                'object_list': 'Проверьте корректность объекта в БД. Невозможно выгрузить объект',
                'is_error': 1
            })


def get_object_error_msg_view(request, object_type: str, object_name: str):
    template_name = 'ddl_objects/error_detail.html'
    try:
        queryset = services.get_object_error_msg_service(object_type, object_name)
        return render(request, template_name, {'error_list': queryset})
    except cx_Oracle.DatabaseError as e:
        return render(request, template_name, {
            'object_list': 'Проверьте корректность объекта в БД. Невозможно выгрузить объект',
            'is_error': 1
        })


def download_object_ddl(request):
    object_type = 'TABLE'
    object_name = 'DR_AGC_STATUS'
    try:
        queryset = services.get_object_ddl_script_service(object_type, object_name)

        response = HttpResponse(queryset, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}.sql'.format(object_name)
        return response
    except cx_Oracle.DatabaseError as e:
        return


def get_files(request):
    import yaml
    sa = None
    asd = yaml.safe_load(sa)
    asd.keys()

    root_dir = 'DWH_DDS'
    object_type = 'TABLE'
    object_name = 'DR_AGC_STATUS'
    objects = {}
    tables = {}
    packages = {}
    procedures = {}
    functions = {}
    sequences = {}
    indexes = {}

    dc = {'dwh_dds': {'table': ['DR_AGC_STATUS', 'DRIVER', 'DR_AGC_AVR_TYPE'],
                      'package': ['PKG_TRANSACTION_MASTER_DICT', 'PKG_TRANSFORM_LOSS']}}

    try:
        if db_conf.DBSchema.DWH_DDS.name in [k.upper() for k in dc.keys()]:
            objects[db_conf.DBSchema.DWH_DDS.name] = []

            if 'table' in dc['dwh_dds']:
                for tab in dc['dwh_dds']['table']:
                    tables[tab] = services.get_object_ddl_script_service('table', tab)
            objects['dwh_dds'].append({'tables': tables})

            if 'package' in dc['dwh_dds']:
                for pack in dc['dwh_dds']['package']:
                    packages[pack] = services.get_object_ddl_script_service('package', pack)
            objects['dwh_dds'].append({'packages': packages})

    # try:
        # queryset = get_object_ddl_script_service(object_type, object_name)

        s = utils.zipper('dwh_dds', 'tables', tables)

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s, content_type="application/zip")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=patch.zip'

        return resp
    except cx_Oracle.DatabaseError as e:
        return
