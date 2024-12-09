from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from datetime import datetime, timedelta
from django.db.models import Q

# Create your views here.
#Generacion de deuda de los gastos comunes

def generar_gasto (request, mes = None, anio = None):
    monto = 850000
    try:
        if mes and anio:
            fechadeuda = datetime(int(anio), int(mes), 1)
            for depto in Residente.objects.all():
                Deuda.objects.create(monto = monto,fechadeuda=fechadeuda, fechavencimiento = fechadeuda + timedelta(days=15))
        elif anio: 
            for mes in range(1,13):
                fechadeuda = datetime(int(anio),mes,1)
                for depto in Residente.objects.all():
                    Deuda.objects.create(monto = monto,fechadeuda= fechadeuda,fechavencimiento = fechadeuda +timedelta(days=15))
        
        return JsonResponse({'success' : True})
    except Exception as e: 
        return JsonResponse({'success': False})
    
def obtener_pagos(request, rut, mes, anio):
    try:

        residente = Residente.objects.get(rut=rut)

        pago = Pago.objects.filter(
            residente=residente,
            fechapago__month=mes,
            fechapago__year=anio
        )

        if pago.exists():
            pagos = [
                {
                    'id': boleta.pk,
                    'monto': boleta.monto,
                    'fecha': boleta.fechapago,
                    'residente': boleta.residente.persona.rut
                }
                for boleta in pago
            ]
            return JsonResponse({'success': True, 'pagos': pagos})
        else:
            return JsonResponse({'success': False, 'message': 'No se encontraron pagos'})
    except Residente.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Residente no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def pendientes(request, mes, anio):
    try:
        limite = datetime(int(anio), int(mes), 1)

        deudas = Deuda.objects.filter(
            fechavencimiento__lte=limite,
            montodeuda__gt=0
        ).order_by('fechavencimiento')

        if not deudas.exists():
            return JsonResponse({'success': False, 'message': 'No se encontraron deudas pendientes'})
        
        deudas_pendientes = [
            {
                'id': deuda.pk,
                'monto': deuda.montodeuda,
                'fecha': deuda.fechavencimiento,
                'residente': deuda.pago.residente.persona.rut
            }
            for deuda in deudas
        ]

        return JsonResponse({'success': True, 'deudas': deudas_pendientes})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def deudas_residente(request, rut):
    try:
        residente = Residente.objects.get(rut=rut)

        deudas = Deuda.objects.filter(
            pago__residente=residente,
            montodeuda__gt=0
        ).order_by('fechavencimiento')

        if not deudas.exists():
            return JsonResponse({'success': False, 'message': 'No se encontraron deudas pendientes'})
        
        deudas_residente = [
            {
                'id': deuda.pk,
                'monto': deuda.montodeuda,
                'fecha': deuda.fechavencimiento,
                'residente': deuda.pago.residente.persona.rut
            }
            for deuda in deudas
        ]

        return JsonResponse({'success': True, 'deudas': deudas_residente})
    
    except Residente.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Residente no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def pagos(request, mes, anio):
    try:
        limite = datetime(int(anio), int(mes), 1)

        pagos = Pago.objects.filter(
            fechapago__month=mes,
            fechapago__year=anio
        ).order_by('fechapago')

        if not pagos.exists():
            return JsonResponse({'success': False, 'message': 'No se encontraron pagos'})
        
        pagos_mes = [
            {
                'id': pago.pk,
                'monto': pago.monto,
                'fecha': pago.fechapago,
                'residente': pago.residente.persona.rut
            }
            for pago in pagos
        ]

        return JsonResponse({'success': True, 'pagos': pagos_mes})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def deudas_expiradas(request):
    try:
        hoy = timezone.now()

        deudas = Deuda.objects.filter(
            fechavencimiento__lt=hoy,
            montodeuda__gt=0
        ).order_by('fechavencimiento')

        if not deudas.exists():
            return JsonResponse({'success': False, 'message': 'No se encontraron deudas expiradas'})
        
        deudas_expiradas = [
            {
                'id': deuda.pk,
                'monto': deuda.montodeuda,
                'fecha': deuda.fechavencimiento,
                'residente': deuda.pago.residente.persona.rut
            }
            for deuda in deudas
        ]

        return JsonResponse({'success': True, 'deudas': deudas_expiradas})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def historial(request):
    try:
        pagos = Pago.objects.all().order_by('fechapago')

        if not pagos.exists():
            return JsonResponse({'success': False, 'message': 'No se encontraron pagos'})
        
        historial = [
            {
                'id': pago.pk,
                'monto': pago.monto,
                'fecha': pago.fechapago,
                'residente': pago.residente.persona.rut
            }
            for pago in pagos
        ]

        return JsonResponse({'success': True, 'historial': historial})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

