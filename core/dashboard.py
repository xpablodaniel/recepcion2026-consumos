"""
Módulo para gestionar el dashboard de habitaciones del hotel.
Calcula estados y colores según ocupación y consumos.
"""

import pandas as pd
import os
from datetime import datetime

# Estructura del hotel
PISOS = {
    1: list(range(101, 122)),  # 101-121 (21 habitaciones)
    2: list(range(222, 243)),  # 222-242 (21 habitaciones)
    3: list(range(343, 354)),  # 343-353 (11 habitaciones)
}

def obtener_habitaciones_ocupadas(archivo_pasajeros='data/pasajeros.csv'):
    """
    Obtiene la lista de habitaciones ocupadas desde el CSV de pasajeros.
    Retorna un diccionario con número de habitación como key y datos del pasajero.
    """
    if not os.path.exists(archivo_pasajeros):
        return {}
    
    df = pd.read_csv(archivo_pasajeros)
    habitaciones_ocupadas = {}
    
    for _, row in df.iterrows():
        habitaciones_ocupadas[int(row['Nro. habitación'])] = {
            'pasajero': row['Apellido y nombre'],
            'plazas': int(row['Plazas ocupadas']),
            'ingreso': row['Fecha de ingreso'],
            'egreso': row['Fecha de egreso'],
            'servicios': row['Servicios']
        }
    
    return habitaciones_ocupadas


def obtener_habitaciones_con_consumos(archivo_consumos='data/consumos_diarios.csv'):
    """
    Obtiene la lista de habitaciones que tienen consumos registrados.
    Retorna un set con los números de habitación.
    """
    if not os.path.exists(archivo_consumos):
        return set()
    
    df = pd.read_csv(archivo_consumos)
    return set(df['habitacion'].astype(int).unique())


def es_checkout_hoy(fecha_egreso):
    """
    Verifica si la fecha de egreso es hoy.
    Formato esperado: DD/MM/YYYY
    """
    try:
        fecha_hoy = datetime.now().strftime('%d/%m/%Y')
        return fecha_egreso == fecha_hoy
    except:
        return False


def obtener_habitaciones_checkout():
    """
    Obtiene las habitaciones con checkout programado para hoy.
    Retorna un set con los números de habitación.
    """
    habitaciones_ocupadas = obtener_habitaciones_ocupadas()
    checkouts_hoy = set()
    
    for num_hab, datos in habitaciones_ocupadas.items():
        if es_checkout_hoy(datos['egreso']):
            checkouts_hoy.add(num_hab)
    
    return checkouts_hoy


def calcular_estado_habitacion(num_habitacion, habitaciones_ocupadas, habitaciones_con_consumos, checkouts_hoy=None):
    """
    Calcula el estado de una habitación según su ocupación y consumos.
    
    Retorna:
        - 'vacia': habitación no ocupada (gris)
        - 'ocupada': ocupada sin consumos (verde)
        - 'con_consumos': ocupada con consumos (naranja)
        - 'checkout': checkout programado para hoy (rojo)
    """
    if num_habitacion not in habitaciones_ocupadas:
        return 'vacia'
    
    # Prioridad 1: Check-out hoy
    if checkouts_hoy and num_habitacion in checkouts_hoy:
        return 'checkout'
    
    # Prioridad 2: Con consumos
    if num_habitacion in habitaciones_con_consumos:
        return 'con_consumos'
    
    # Por defecto: ocupada sin consumos
    return 'ocupada'


def obtener_datos_dashboard():
    """
    Obtiene todos los datos necesarios para renderizar el dashboard.
    
    Retorna un diccionario con:
        - pisos: estructura de habitaciones por piso
        - estados: estado de cada habitación
        - ocupadas: datos de habitaciones ocupadas
        - estadisticas: resumen general
        - checkouts_hoy: habitaciones con checkout hoy
    """
    habitaciones_ocupadas = obtener_habitaciones_ocupadas()
    habitaciones_con_consumos = obtener_habitaciones_con_consumos()
    checkouts_hoy = obtener_habitaciones_checkout()
    
    # Calcular estados de todas las habitaciones
    estados = {}
    for piso, habitaciones in PISOS.items():
        for num_hab in habitaciones:
            estados[num_hab] = calcular_estado_habitacion(
                num_hab, 
                habitaciones_ocupadas, 
                habitaciones_con_consumos,
                checkouts_hoy
            )
    
    # Calcular estadísticas
    total_habitaciones = sum(len(habs) for habs in PISOS.values())
    total_ocupadas = len(habitaciones_ocupadas)
    total_con_consumos = len([h for h, e in estados.items() if e == 'con_consumos'])
    total_checkouts = len(checkouts_hoy)
    
    estadisticas = {
        'total': total_habitaciones,
        'ocupadas': total_ocupadas,
        'vacias': total_habitaciones - total_ocupadas,
        'con_consumos': total_con_consumos,
        'sin_consumos': total_ocupadas - total_con_consumos,
        'checkouts_hoy': total_checkouts
    }
    
    return {
        'pisos': PISOS,
        'estados': estados,
        'ocupadas': habitaciones_ocupadas,
        'estadisticas': estadisticas,
        'checkouts_hoy': checkouts_hoy
    }


def obtener_total_consumos_habitacion(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Calcula el total de consumos de una habitación específica.
    """
    if not os.path.exists(archivo_consumos):
        return 0
    
    df = pd.read_csv(archivo_consumos)
    consumos_hab = df[df['habitacion'] == num_habitacion]
    
    if consumos_hab.empty:
        return 0
    
    return consumos_hab['monto'].sum()
