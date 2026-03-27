from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agendar/', views.agendar, name='agendar'),
    path('agendar/pendiente/', views.cita_pendiente, name='cita_pendiente'),
    path('confirmar/<uuid:token>/', views.confirmar_cita, name='confirmar'),
    path('citas/', views.lista_citas, name='lista_citas'),
]
