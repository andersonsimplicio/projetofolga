from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', homecoord, name='homecood'),
    path('login/', loginCoordenador, name='login'),
    path('cad_coord', CadCoordView.as_view(), name='cad_coord'),
    path('logout_manager/', logout_view, name='logout_manager'),
    path('cadastro/', cad_func, name='cad_func'),
    path('listar_func/', listar_func, name='listar_func'),
    path('listar_func/apagar/<str:id>', apagar_func, name='apagar_func'),
    path('listar_func/update_func/<int:id>', update_func, name='update_func'),
    path('cad_plantao', PlantaoView.as_view(), name='cad_plantao'),
    path('plantao_dia', PlantaoDiaView.as_view(), name='plantao_dia'),
    path('apagar_plantao/<str:data>/<str:turno>',
         apagar_plantao, name='apagar_plantao'),
    path('pdf/', pdf_view, name='pdf'),
    path('cad_folga', FolgaView.as_view(), name='cad_folga'),
    path('cad_plantao_extra', PlantaoExtraView.as_view(), name='cad_plantao_extra'),
    path('apagar_folgas/<str:plantao>/<str:data>',
         clean_dayoff, name='apagar_folgas'),
    path('buscar', SearchPerDay.as_view(), name='search_per_day'),

]
