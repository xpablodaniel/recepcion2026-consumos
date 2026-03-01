#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para cargar datos de trabajadores ACTIVOS desde consultaRegimenReport.csv
"""

import pandas as pd
from datetime import datetime

# Leer el CSV de trabajadores activos
df = pd.read_csv('data/consultaRegimenReport.csv')

print(f"\n📊 CSV cargado: {len(df)} registros encontrados")
print(f"Habitaciones únicas: {df['Nro. habitación'].nunique()}")

# Crear estructura para pasajeros.csv
pasajeros = []

for _, row in df.iterrows():
    pasajero = {
        'nombre': row['Apellido y nombre'],
        'documento': str(row['Nro. doc.']),
        'edad': int(row['Edad']) if pd.notna(row['Edad']) else 0,
        'habitacion': int(row['Nro. habitación']),
        'tipo_habitacion': row['Tipo habitación'],
        'voucher': str(row['Voucher']),
        'sede': row['Sede'],
        'ingreso': row['Fecha de ingreso'],
        'egreso': row['Fecha de egreso'],
        'servicios': row['Servicios'],
        'plazas': int(row['Plazas ocupadas']) if pd.notna(row['Plazas ocupadas']) else 0
    }
    pasajeros.append(pasajero)

# Crear DataFrame
df_pasajeros = pd.DataFrame(pasajeros)

# Ordenar por habitación y nombre
df_pasajeros = df_pasajeros.sort_values(['habitacion', 'nombre'])

# Guardar en pasajeros.csv
df_pasajeros.to_csv('data/pasajeros.csv', index=False)

print(f"\n✅ Archivo pasajeros.csv generado exitosamente")
print(f"\n📋 Resumen:")
print(f"   • Total pasajeros: {len(df_pasajeros)}")
print(f"   • Total habitaciones: {df_pasajeros['habitacion'].nunique()}")
print(f"   • Período: {df_pasajeros['ingreso'].min()} - {df_pasajeros['egreso'].max()}")

# Mostrar algunas estadísticas
print(f"\n📊 Estadísticas:")
print(f"   • Vouchers únicos: {df_pasajeros['voucher'].nunique()}")
print(f"   • Sedes representadas: {df_pasajeros['sede'].nunique()}")

# Mostrar tipos de régimen
print(f"\n🍽️ Tipos de servicio:")
print(df_pasajeros['servicios'].value_counts().to_string())

# Mostrar primeros registros
print(f"\n👥 Primeros 5 registros:")
print(df_pasajeros[['habitacion', 'nombre', 'voucher', 'ingreso', 'egreso']].head().to_string())

print("\n✅ ¡Listo! Datos de trabajadores activos cargados correctamente")
print("📌 Características: Check-out anticipado disponible, vienen por sus medios")
