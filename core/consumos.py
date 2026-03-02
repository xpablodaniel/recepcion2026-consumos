"""
Módulo para gestionar operaciones de consumos individuales por habitación.
"""

import pandas as pd
import os
from datetime import datetime
from pandas.errors import EmptyDataError


def obtener_consumos_habitacion(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Obtiene todos los consumos de una habitación específica.
    
    Returns:
        DataFrame con los consumos ordenados por fecha
    """
    if not os.path.exists(archivo_consumos):
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(archivo_consumos)
    except EmptyDataError:
        return pd.DataFrame(columns=['fecha', 'habitacion', 'pasajero', 'categoria', 'monto'])

    if df.empty or 'habitacion' not in df.columns:
        return pd.DataFrame(columns=['fecha', 'habitacion', 'pasajero', 'categoria', 'monto'])

    consumos_hab = df[df['habitacion'] == num_habitacion].copy()
    
    # Agregar índice para identificar cada consumo
    if not consumos_hab.empty:
        consumos_hab['indice'] = range(len(consumos_hab))
    
    return consumos_hab


def obtener_total_consumos(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Calcula el total de consumos de una habitación.
    
    Returns:
        Diccionario con totales por categoría y total general
    """
    consumos = obtener_consumos_habitacion(num_habitacion, archivo_consumos)
    
    if consumos.empty:
        return {
            'Bebidas': 0,
            'Estadía': 0,
            'Map': 0,
            'total': 0
        }
    
    totales = {
        'Bebidas': consumos[consumos['categoria'] == 'Bebidas']['monto'].sum() if 'Bebidas' in consumos['categoria'].values else 0,
        'Estadía': consumos[consumos['categoria'] == 'Estadía']['monto'].sum() if 'Estadía' in consumos['categoria'].values else 0,
        'Map': consumos[consumos['categoria'] == 'Map']['monto'].sum() if 'Map' in consumos['categoria'].values else 0,
    }
    totales['total'] = sum(totales.values())
    
    return totales


def obtener_consumos_por_pasajero(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Agrupa los consumos de una habitación por pasajero individual.
    Útil cuando hay múltiples personas con distintos vouchers en una habitación.
    
    Args:
        num_habitacion (int): Número de habitación
        archivo_consumos (str): Ruta al archivo CSV de consumos
    
    Returns:
        Diccionario donde la key es el nombre del pasajero y el valor es:
        {
            'consumos': lista de consumos,
            'totales': diccionario con totales por categoría,
            'total_general': suma total
        }
    """
    consumos = obtener_consumos_habitacion(num_habitacion, archivo_consumos)
    
    if consumos.empty:
        return {}
    
    consumos_por_pasajero = {}
    
    for _, row in consumos.iterrows():
        pasajero = row['pasajero']
        
        if pasajero not in consumos_por_pasajero:
            consumos_por_pasajero[pasajero] = {
                'consumos': [],
                'totales': {'Bebidas': 0, 'Estadía': 0, 'Map': 0},
                'total_general': 0
            }
        
        # Agregar consumo a la lista
        consumos_por_pasajero[pasajero]['consumos'].append({
            'indice': row.get('indice', 0),
            'fecha': row['fecha'],
            'categoria': row['categoria'],
            'monto': float(row['monto'])
        })
        
        # Actualizar totales por categoría
        categoria = row['categoria']
        if categoria in consumos_por_pasajero[pasajero]['totales']:
            consumos_por_pasajero[pasajero]['totales'][categoria] += float(row['monto'])
        
        # Actualizar total general
        consumos_por_pasajero[pasajero]['total_general'] += float(row['monto'])
    
    return consumos_por_pasajero


def obtener_total_consumos_pasajero(num_habitacion, nombre_pasajero, archivo_consumos='data/consumos_diarios.csv'):
    """
    Calcula el total de consumos de un pasajero específico en una habitación.
    
    Args:
        num_habitacion (int): Número de habitación
        nombre_pasajero (str): Nombre completo del pasajero
        archivo_consumos (str): Ruta al archivo CSV de consumos
    
    Returns:
        Diccionario con totales por categoría y total general del pasajero
    """
    consumos = obtener_consumos_habitacion(num_habitacion, archivo_consumos)
    
    if consumos.empty:
        return {
            'Bebidas': 0,
            'Estadía': 0,
            'Map': 0,
            'total': 0
        }
    
    # Filtrar solo consumos de este pasajero
    consumos_pasajero = consumos[consumos['pasajero'] == nombre_pasajero]
    
    if consumos_pasajero.empty:
        return {
            'Bebidas': 0,
            'Estadía': 0,
            'Map': 0,
            'total': 0
        }
    
    totales = {
        'Bebidas': consumos_pasajero[consumos_pasajero['categoria'] == 'Bebidas']['monto'].sum() if 'Bebidas' in consumos_pasajero['categoria'].values else 0,
        'Estadía': consumos_pasajero[consumos_pasajero['categoria'] == 'Estadía']['monto'].sum() if 'Estadía' in consumos_pasajero['categoria'].values else 0,
        'Map': consumos_pasajero[consumos_pasajero['categoria'] == 'Map']['monto'].sum() if 'Map' in consumos_pasajero['categoria'].values else 0,
    }
    totales['total'] = sum(totales.values())
    
    return totales


def agregar_consumo(num_habitacion, categoria, monto, pasajero, archivo_consumos='data/consumos_diarios.csv'):
    """
    Agrega un nuevo consumo a una habitación.
    
    Returns:
        True si se agregó correctamente, False en caso contrario
    """
    try:
        nuevo_registro = {
            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'habitacion': num_habitacion,
            'pasajero': pasajero,
            'categoria': categoria,
            'monto': float(monto)
        }
        
        df_nuevo = pd.DataFrame([nuevo_registro])
        
        if os.path.exists(archivo_consumos):
            df_nuevo.to_csv(archivo_consumos, mode='a', header=False, index=False)
        else:
            df_nuevo.to_csv(archivo_consumos, mode='w', header=True, index=False)
        
        return True
    except Exception as e:
        print(f"Error al agregar consumo: {e}")
        return False


def eliminar_consumo_por_indice(num_habitacion, indice, archivo_consumos='data/consumos_diarios.csv'):
    """
    Elimina un consumo específico de una habitación por su índice.
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    try:
        if not os.path.exists(archivo_consumos):
            return False
        
        df = pd.read_csv(archivo_consumos)
        consumos_hab = df[df['habitacion'] == num_habitacion]
        
        if indice >= len(consumos_hab):
            return False
        
        # Obtener el índice global del consumo a eliminar
        indice_global = consumos_hab.index[indice]
        
        # Eliminar la fila
        df = df.drop(indice_global)
        
        # Guardar el archivo
        df.to_csv(archivo_consumos, index=False)
        
        return True
    except Exception as e:
        print(f"Error al eliminar consumo: {e}")
        return False


def obtener_resumen_habitacion(num_habitacion, datos_pasajero, archivo_consumos='data/consumos_diarios.csv'):
    """
    Obtiene un resumen completo de la habitación incluyendo pasajero y consumos.
    Incluye consumos separados por pasajero cuando hay múltiples personas.
    
    Args:
        num_habitacion (int): Número de habitación
        datos_pasajero (dict): Datos del titular de la habitación
        archivo_consumos (str): Ruta al archivo CSV de consumos
    
    Returns:
        Diccionario con toda la información de la habitación
    """
    from core.dashboard import obtener_todos_pasajeros_habitacion
    
    consumos = obtener_consumos_habitacion(num_habitacion, archivo_consumos)
    totales = obtener_total_consumos(num_habitacion, archivo_consumos)
    
    # Obtener TODOS los pasajeros de la habitación
    todos_pasajeros = obtener_todos_pasajeros_habitacion(num_habitacion)
    
    # Obtener consumos agrupados por pasajero
    consumos_por_pasajero = obtener_consumos_por_pasajero(num_habitacion, archivo_consumos)
    
    # Convertir consumos a lista de diccionarios para el template
    lista_consumos = []
    if not consumos.empty:
        for idx, row in consumos.iterrows():
            lista_consumos.append({
                'indice': row.get('indice', 0),
                'fecha': row['fecha'],
                'pasajero': row['pasajero'],
                'categoria': row['categoria'],
                'monto': row['monto']
            })
    
    # Detectar si hay múltiples vouchers (personas que no se conocen)
    vouchers_unicos = set(p['voucher'] for p in todos_pasajeros)
    tiene_vouchers_separados = len(vouchers_unicos) > 1 and len(todos_pasajeros) > 1
    
    return {
        'numero': num_habitacion,
        'pasajero': datos_pasajero,
        'todos_pasajeros': todos_pasajeros,
        'consumos': lista_consumos,
        'consumos_por_pasajero': consumos_por_pasajero,
        'totales': totales,
        'cantidad_consumos': len(lista_consumos),
        'tiene_vouchers_separados': tiene_vouchers_separados,
        'cantidad_pasajeros': len(todos_pasajeros)
    }
