from django.urls import path
from . import views


urlpatterns = [
    path('', views.GetTablesView.as_view(), name='tables_page'),
    path('procedures', views.GetProceduresView.as_view(), name='procedures_page'),
    path('functions', views.GetFunctionsView.as_view(), name='functions_page'),
    path('packages', views.GetPackagesView.as_view(), name='packages_page'),
    path('sequences', views.GetSequencesView.as_view(), name='sequences_page'),

    path('object/<str:object_type>/<str:object_name>', views.get_object_ddl_script, name='object_detail'),
    path('error/<str:object_type>/<str:object_name>', views.get_object_error_msg_view, name='error_detail'),

    # path('get_files', views.download_object_ddl, name='download_zip'),
    path('get_files', views.get_files, name='download_zip'),
]
