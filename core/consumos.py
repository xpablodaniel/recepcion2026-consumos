"""
Módulo para gestionar operaciones de consumos individuales por habitación.
"""

import pandas as pd
import os
from datetime import datetime


def obtener_consumos_habitacion(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Obtiene todos los consumos de una habitación específica.
    
    Returns:
        DataFrame con los consumos ordenados por fecha
    """
    if not os.path.exists(archivo_consumos):
        return pd.DataFrame()
    
    df = pd.read_csv(archivo_consumos)
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
    
    Returns:
        Diccionario con toda la información de la habitación
    """
    consumos = obtener_consumos_habitacion(num_habitacion, archivo_consumos)
    totales = obtener_total_consumos(num_habitacion, archivo_consumos)
    
    # Convertir consumos a lista de diccionarios para el template
    lista_consumos = []
    if not consumos.empty:
        for idx, row in consumos.iterrows():
            lista_consumos.append({
                'indice': row.get('indice', 0),
                'fecha': row['fecha'],
                'categoria': row['categoria'],
                'monto': row['monto']
            })
    
    return {
        'numero': num_habitacion,
        'pasajero': datos_pasajero,
        'consumos': lista_consumos,
        'totales': totales,
        'cantidad_consumos': len(lista_consumos)
    }
