from django.db import models


class TableCustomManager(models.Manager):
    """Менеджер таблиц. Добавляет фильтр по таблицам для queryset"""
    def get_queryset(self):
        return super().get_queryset().filter(object_type='TABLE')


class ProcedureCustomManager(models.Manager):
    """Менеджер таблиц. Добавляет фильтр по процедурам для queryset"""
    def get_queryset(self):
        return super().get_queryset().filter(object_type='PROCEDURE')


class FunctionCustomManager(models.Manager):
    """Менеджер таблиц. Добавляет фильтр по функциям для queryset"""
    def get_queryset(self):
        return super().get_queryset().filter(object_type='FUNCTION')


class PackageCustomManager(models.Manager):
    """Менеджер таблиц. Добавляет фильтр по пакетам для queryset"""
    def get_queryset(self):
        return super().get_queryset().filter(object_type='PACKAGE')


class SequenceCustomManager(models.Manager):
    """Менеджер таблиц. Добавляет фильтр по сиквенцам для queryset"""
    def get_queryset(self):
        return super().get_queryset().filter(object_type='SEQUENCE')


class BaseObject(models.Model):
    """Базовый объект БД"""
    object_name = models.CharField("Название", max_length=250, primary_key=True)
    owner = models.CharField("Владелец", max_length=250)
    object_type = models.CharField("Тип объекта", max_length=250)
    status = models.CharField("Статус", max_length=250)
    created = models.DateTimeField("Дата создания")
    last_ddl_time = models.DateTimeField("Дата компиляции")

    def __str__(self):
        return self.object_name

    all_tables = TableCustomManager()
    all_procedures = ProcedureCustomManager()
    all_functions = FunctionCustomManager()
    all_packages = PackageCustomManager()
    all_sequences = SequenceCustomManager()

    class Meta:
        db_table = 'ALL_OBJECTS'
        managed = False
        ordering = ['object_name']
