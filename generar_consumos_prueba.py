#!/usr/bin/env python3
"""
Script para generar consumos de prueba simulando una temporada completa
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Archivos
DB_PASAJEROS = 'pasajeros.csv'
DB_CONSUMOS = 'consumos_diarios.csv'

# Leer pasajeros activos
df_pasajeros = pd.read_csv(DB_PASAJEROS)

# Categorías y rangos de precios realistas
categorias_precios = {
    'Bebidas': (500, 3500),      # Bebidas desde $500 a $3500
    'Estadía': (15000, 45000),   # Estadía desde $15000 a $45000
    'Map': (8000, 25000)          # Map desde $8000 a $25000
}

# Lista para acumular consumos
consumos = []

print("🏨 Generando consumos de prueba para la temporada...")
print("=" * 60)

# Generar consumos para cada pasajero
for idx, pasajero in df_pasajeros.iterrows():
    habitacion = pasajero['Nro. habitación']
    nombre = pasajero['Apellido y nombre']
    fecha_ingreso = datetime.strptime(pasajero['Fecha de ingreso'], '%d/%m/%Y')
    fecha_egreso = datetime.strptime(pasajero['Fecha de egreso'], '%d/%m/%Y')
    
    # Calcular días de estadía
    dias_estadia = (fecha_egreso - fecha_ingreso).days
    
    print(f"\n📋 Hab {habitacion} - {nombre}")
    print(f"   Estadía: {dias_estadia} días ({fecha_ingreso.strftime('%d/%m')} al {fecha_egreso.strftime('%d/%m')})")
    
    # ESTADÍA: Siempre una vez al final
    monto_estadia = random.randint(categorias_precios['Estadía'][0], categorias_precios['Estadía'][1])
    fecha_estadia = fecha_egreso - timedelta(hours=random.randint(8, 12))
    consumos.append({
        'fecha': fecha_estadia.strftime('%d/%m/%Y %H:%M'),
        'habitacion': habitacion,
        'pasajero': nombre,
        'categoria': 'Estadía',
        'monto': monto_estadia
    })
    print(f"   ✅ Estadía: ${monto_estadia:,}")
    
    # MAP: 1-2 veces durante la estadía
    if dias_estadia >= 2:
        num_maps = random.randint(1, min(2, dias_estadia))
        for i in range(num_maps):
            dia_map = random.randint(0, dias_estadia - 1)
            fecha_map = fecha_ingreso + timedelta(days=dia_map, hours=random.randint(12, 20))
            monto_map = random.randint(categorias_precios['Map'][0], categorias_precios['Map'][1])
            consumos.append({
                'fecha': fecha_map.strftime('%d/%m/%Y %H:%M'),
                'habitacion': habitacion,
                'pasajero': nombre,
                'categoria': 'Map',
                'monto': monto_map
            })
        print(f"   ✅ Map: {num_maps} consumo(s)")
    
    # BEBIDAS: 2-5 consumos aleatorios durante la estadía
    num_bebidas = random.randint(2, min(5, dias_estadia * 2))
    total_bebidas = 0
    for i in range(num_bebidas):
        dia_bebida = random.randint(0, dias_estadia)
        fecha_bebida = fecha_ingreso + timedelta(days=dia_bebida, hours=random.randint(10, 23), minutes=random.randint(0, 59))
        monto_bebida = random.randint(categorias_precios['Bebidas'][0], categorias_precios['Bebidas'][1])
        total_bebidas += monto_bebida
        consumos.append({
            'fecha': fecha_bebida.strftime('%d/%m/%Y %H:%M'),
            'habitacion': habitacion,
            'pasajero': nombre,
            'categoria': 'Bebidas',
            'monto': monto_bebida
        })
    print(f"   ✅ Bebidas: {num_bebidas} consumo(s) - Total: ${total_bebidas:,}")

# Ordenar por fecha
df_consumos = pd.DataFrame(consumos)
df_consumos['fecha_ordenamiento'] = pd.to_datetime(df_consumos['fecha'], format='%d/%m/%Y %H:%M')
df_consumos = df_consumos.sort_values('fecha_ordenamiento')
df_consumos = df_consumos.drop('fecha_ordenamiento', axis=1)

# Guardar en CSV
df_consumos.to_csv(DB_CONSUMOS, index=False)

print("\n" + "=" * 60)
print(f"✅ Se generaron {len(consumos)} consumos para {len(df_pasajeros)} habitaciones")
print(f"📁 Archivo guardado: {DB_CONSUMOS}")
print("\n📊 Resumen por categoría:")
resumen = df_consumos.groupby('categoria')['monto'].agg(['count', 'sum'])
for categoria, datos in resumen.iterrows():
    print(f"   • {categoria}: {int(datos['count'])} consumos - Total: ${datos['sum']:,.0f}")

print(f"\n💰 Total general: ${df_consumos['monto'].sum():,.0f}")
print("=" * 60)
print("\n🎯 Ahora puedes probar las funciones de cierre y exportación!")
