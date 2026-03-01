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

# Crear estructura para pasajeros.csv con nombres de columnas compatibles
pasajeros = []

for _, row in df.iterrows():
    pasajero = {
        'Apellido y nombre': row['Apellido y nombre'],
        'Nro. doc.': str(row['Nro. doc.']),
        'Edad': int(row['Edad']) if pd.notna(row['Edad']) else 0,
        'Nro. habitación': int(row['Nro. habitación']),
        'Tipo habitación': row['Tipo habitación'],
        'Voucher': str(row['Voucher']),
        'Sede': row['Sede'],
        'Fecha de ingreso': row['Fecha de ingreso'],
        'Fecha de egreso': row['Fecha de egreso'],
        'Servicios': row['Servicios'],
        'Plazas ocupadas': int(row['Plazas ocupadas']) if pd.notna(row['Plazas ocupadas']) else 0
    }
    pasajeros.append(pasajero)

# Crear DataFrame
df_pasajeros = pd.DataFrame(pasajeros)

# Ordenar por habitación y nombre
df_pasajeros = df_pasajeros.sort_values(['Nro. habitación', 'Apellido y nombre'])

# Guardar en pasajeros.csv
df_pasajeros.to_csv('data/pasajeros.csv', index=False)

print(f"\n✅ Archivo pasajeros.csv generado exitosamente")
print(f"\n📋 Resumen:")
print(f"   • Total pasajeros: {len(df_pasajeros)}")
print(f"   • Total habitaciones: {df_pasajeros['Nro. habitación'].nunique()}")
print(f"   • Período: {df_pasajeros['Fecha de ingreso'].min()} - {df_pasajeros['Fecha de egreso'].max()}")

# Mostrar algunas estadísticas
print(f"\n📊 Estadísticas:")
print(f"   • Vouchers únicos: {df_pasajeros['Voucher'].nunique()}")
print(f"   • Sedes representadas: {df_pasajeros['Sede'].nunique()}")

# Mostrar tipos de régimen
print(f"\n🍽️ Tipos de servicio:")
print(df_pasajeros['Servicios'].value_counts().to_string())

# Mostrar primeros registros
print(f"\n👥 Primeros 5 registros:")
print(df_pasajeros[['Nro. habitación', 'Apellido y nombre', 'Voucher', 'Fecha de ingreso', 'Fecha de egreso']].head().to_string())

print("\n✅ ¡Listo! Datos de trabajadores activos cargados correctamente")
print("📌 Características: Check-out anticipado disponible, vienen por sus medios")
