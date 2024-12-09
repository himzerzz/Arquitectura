from django.urls import path
from . import views

urlpatterns = [
    path('gastos/<int:mes>/<int:anio>',  views.generar_gasto),
    path('pagos/<int:rut>/<int:mes>/<int:anio>', views.obtener_pagos),
    path('pendientes/<int:mes>/<int:anio>', views.pendientes)
]
