from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'compta'
urlpatterns = [
    url(r'^$', views.index_operations, name='index'),
    url(r'^export/(.*)', views.export_operations, name='export'),
    url(r'^excel$', views.export_data_openpyxl, name='export_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
