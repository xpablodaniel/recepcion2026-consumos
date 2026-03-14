"""
Módulo para gestionar operaciones de consumos individuales por habitación.
"""

import pandas as pd
import os
from datetime import datetime
from pandas.errors import EmptyDataError


CONSUMOS_COLUMNS = [
    'fecha',
    'habitacion',
    'pasajero',
    'categoria',
    'item',
    'cantidad',
    'precio_unitario',
    'monto'
]

CANTIDADES_RAPIDAS = [1, 2, 3, 4, 6]

BEBIDAS_CATALOGO = {
    'gaseosa': {'nombre': 'Gaseosa', 'icono': '🥤', 'precio': 3500.0},
    'agua': {'nombre': 'Agua', 'icono': '💧', 'precio': 3000.0},
    'saborizada': {'nombre': 'Saborizada', 'icono': '🧃', 'precio': 3300.0},
    'cerveza': {'nombre': 'Cerveza', 'icono': '🍺', 'precio': 5500.0},
    'nampe_malbec': {'nombre': 'Nampe Malbec', 'icono': '🍷', 'precio': 6500.0},
    'chacabuco_chenin': {'nombre': 'Chacabuco Chenin', 'icono': '🍷', 'precio': 8000.0},
    'chacabuco_malbec': {'nombre': 'Chacabuco Malbec', 'icono': '🍷', 'precio': 7800.0},
    'los_haroldos_reserva_malbec': {'nombre': 'Los Haroldos Reserva Malbec', 'icono': '🍷', 'precio': 14800.0},
    'los_haroldos_reserva_chardonnay': {'nombre': 'Los Haroldos Reserva Chardonnay', 'icono': '🍷', 'precio': 14800.0},
    'los_haroldos_estate_malbec': {'nombre': 'Los Haroldos Estate Malbec', 'icono': '🍷', 'precio': 11000.0},
    'los_haroldos_estate_chardonnay': {'nombre': 'Los Haroldos Estate Chardonnay', 'icono': '🍷', 'precio': 11000.0},
}


def obtener_catalogo_bebidas():
    """Retorna el catálogo de bebidas rápidas para la interfaz."""
    catalogo = []
    for codigo, datos in BEBIDAS_CATALOGO.items():
        catalogo.append({
            'codigo': codigo,
            'nombre': datos['nombre'],
            'icono': datos['icono'],
            'precio': datos['precio'],
            'habilitado': datos['precio'] is not None
        })
    return catalogo


def _leer_archivo_consumos(archivo_consumos):
    """Lee el CSV de consumos y garantiza las columnas esperadas."""
    if not os.path.exists(archivo_consumos):
        return pd.DataFrame(columns=CONSUMOS_COLUMNS)

    try:
        df = pd.read_csv(archivo_consumos)
    except EmptyDataError:
        return pd.DataFrame(columns=CONSUMOS_COLUMNS)

    for columna in CONSUMOS_COLUMNS:
        if columna in df.columns:
            continue

        if columna == 'item':
            df[columna] = ''
        elif columna == 'cantidad':
            df[columna] = 1
        elif columna == 'precio_unitario':
            df[columna] = pd.to_numeric(df['monto'], errors='coerce') if 'monto' in df.columns else 0
        else:
            df[columna] = pd.NA

    columnas_ordenadas = CONSUMOS_COLUMNS + [c for c in df.columns if c not in CONSUMOS_COLUMNS]
    return df[columnas_ordenadas]


def obtener_consumos_habitacion(num_habitacion, archivo_consumos='data/consumos_diarios.csv'):
    """
    Obtiene todos los consumos de una habitación específica.
    
    Returns:
        DataFrame con los consumos ordenados por fecha
    """
    df = _leer_archivo_consumos(archivo_consumos)
    
    if df.empty or 'habitacion' not in df.columns:
        return pd.DataFrame(columns=CONSUMOS_COLUMNS)

    habitaciones = pd.to_numeric(df['habitacion'], errors='coerce').fillna(-1).astype(int)
    consumos_hab = df[habitaciones == int(num_habitacion)].copy()
    
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
            'item': '' if pd.isna(row.get('item', '')) else row.get('item', ''),
            'cantidad': '' if pd.isna(row.get('cantidad', '')) else row.get('cantidad', ''),
            'precio_unitario': '' if pd.isna(row.get('precio_unitario', '')) else row.get('precio_unitario', ''),
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
    return agregar_consumo_detallado(
        num_habitacion=num_habitacion,
        categoria=categoria,
        monto=monto,
        pasajero=pasajero,
        archivo_consumos=archivo_consumos
    )


def agregar_consumo_detallado(
    num_habitacion,
    categoria,
    monto,
    pasajero,
    item='',
    cantidad=1,
    precio_unitario=None,
    archivo_consumos='data/consumos_diarios.csv'
):
    """Agrega un consumo permitiendo almacenar item, cantidad y precio unitario."""
    try:
        cantidad = int(cantidad) if cantidad else 1
        monto = float(monto)
        if precio_unitario is None:
            precio_unitario = monto / cantidad if cantidad else monto

        nuevo_registro = {
            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'habitacion': int(num_habitacion),
            'pasajero': pasajero,
            'categoria': categoria,
            'item': item,
            'cantidad': cantidad,
            'precio_unitario': float(precio_unitario),
            'monto': monto
        }

        df = _leer_archivo_consumos(archivo_consumos)
        if df.empty:
            df = pd.DataFrame([nuevo_registro], columns=CONSUMOS_COLUMNS)
        else:
            registro_completo = {columna: pd.NA for columna in df.columns}
            registro_completo.update(nuevo_registro)
            df.loc[len(df)] = registro_completo
        df.to_csv(archivo_consumos, index=False)
        return True
    except Exception as e:
        print(f"Error al agregar consumo: {e}")
        return False


def agregar_consumo_bebida_rapida(num_habitacion, producto_codigo, cantidad, pasajero, archivo_consumos='data/consumos_diarios.csv'):
    """Agrega una bebida rápida usando el catálogo con precios fijos."""
    producto = BEBIDAS_CATALOGO.get(str(producto_codigo).strip().lower())
    if not producto:
        return False, 'Producto de bebida no válido'

    if producto['precio'] is None:
        return False, f"El precio de {producto['nombre']} todavía no está configurado"

    try:
        cantidad = int(cantidad)
    except Exception:
        return False, 'Cantidad inválida'

    if cantidad <= 0:
        return False, 'La cantidad debe ser mayor a cero'

    total = float(producto['precio']) * cantidad
    exito = agregar_consumo_detallado(
        num_habitacion=num_habitacion,
        categoria='Bebidas',
        monto=total,
        pasajero=pasajero,
        item=producto['nombre'],
        cantidad=cantidad,
        precio_unitario=producto['precio'],
        archivo_consumos=archivo_consumos
    )

    if not exito:
        return False, 'No se pudo registrar la bebida'

    return True, f"{cantidad} x {producto['nombre']} agregado(s) a {pasajero} por ${total:,.0f}"


def eliminar_consumo_por_indice(num_habitacion, indice, archivo_consumos='data/consumos_diarios.csv'):
    """
    Elimina un consumo específico de una habitación por su índice.
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    try:
        df = _leer_archivo_consumos(archivo_consumos)
        if df.empty:
            return False

        habitaciones = pd.to_numeric(df['habitacion'], errors='coerce').fillna(-1).astype(int)
        consumos_hab = df[habitaciones == int(num_habitacion)]
        
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
            item = row.get('item', '')
            cantidad = row.get('cantidad', '')
            precio_unitario = row.get('precio_unitario', '')

            if pd.isna(item):
                item = ''
            if pd.isna(cantidad):
                cantidad = ''
            if pd.isna(precio_unitario):
                precio_unitario = ''

            lista_consumos.append({
                'indice': row.get('indice', 0),
                'fecha': row['fecha'],
                'pasajero': row['pasajero'],
                'categoria': row['categoria'],
                'item': item,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
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
