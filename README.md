# 🏨 Sistema de Gestión Hotelera - Recepción 2026

Sistema automatizado integral para la gestión de reservas y consumos de hotel.

## � Instalación

### Ubuntu Nativo
Para instalación en Ubuntu nativo con acceso directo en escritorio, consulta: **[INSTALACION_UBUNTU.md](INSTALACION_UBUNTU.md)**

### WSL/Windows
Sigue las instrucciones de uso en la sección correspondiente más abajo.

## �📋 Descripción

Este repositorio contiene herramientas Python para automatizar la gestión hotelera completa:

### 🍹 Sistema de Consumos (NUEVO)
- ✅ Registro web de consumos diarios por habitación
- ✅ 3 categorías: Bebidas, Estadía, Map
- ✅ Generación automática de reportes Excel (salidas.xlsx)
- ✅ Validación de habitaciones contra pasajeros activos
- ✅ Archivo de temporada con backup automático
- ✅ Interfaz web intuitiva con Bootstrap 5

### 📊 Sistema de Reservas
- Importar datos desde archivos CSV exportados del sistema de gestión
- Distribuir automáticamente los pasajeros en las grillas de cada piso
- Generar estadísticas dinámicas de ocupación
- Limpiar y reiniciar las grillas preservando la estructura

## 🏢 Estructura del Hotel

- **PISO 1**: Habitaciones 101-121 (21 habitaciones)
- **PISO 2**: Habitaciones 222-242 (21 habitaciones)
- **PISO 3**: Habitaciones 343-353 (11 habitaciones)
- **Total**: 53 habitaciones

## 🚀 Uso

### Sistema de Consumos (Web App)

#### Inicio Rápido

**Opción 1: Acceso Directo desde Escritorio**
```bash
# Doble clic en el icono "Sistema Recepción 2026" del escritorio
```

**Opción 2: Script automatizado (Ubuntu Nativo)**
```bash
./run_hotel.sh  # Crea venv, instala dependencias y abre navegador automáticamente
```

**Opción 3: Línea de comandos (WSL/Manual)**
```bash
./iniciar_recepcion.sh  # Requiere entorno virtual ya configurado
```

Luego accede desde tu navegador a: **http://localhost:5000**

#### Funcionalidades

**1. Cargar Consumos**
- Selecciona número de habitación (valida contra pasajeros.csv)
- Elige categoría: Bebidas, Estadía o Map
- Ingresa el monto
- El sistema registra fecha/hora automáticamente

**2. Consulta Diaria (CSV)**
- Genera tabla pivote con totales por habitación y categoría
- Descarga: `consulta_consumos_DD-MM-YYYY.csv`
- Columnas: HAB, Bebidas, Estadía, Map, TOTAL_GENERAL

**3. Generar Salidas XLSX**
- Genera archivo Excel formato salidas.ods
- Distribución en columnas por categoría
- Estructura:
  - Columna 1: HAB
  - Columna 2: Estadía  
  - Columna 3: Map
  - Columna 4: Bebidas
  - Columna 5: Forma de pago
  - Columna 6: Total
- Descarga: `salidas_DD-MM-YYYY.xlsx`

**4. Ver Consumos**
- Historial completo de todas las transacciones
- Filtrable en el navegador

**5. Reiniciar Temporada**
- Crea backup: `consumos_diarios_BACKUP_DD-MM-YYYY_HH-MM.csv`
- Limpia la base de datos actual
- Mantiene estructura para nueva temporada

#### Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está corriendo el servidor.

---

### Sistema de Reservas (Scripts Python)

### 1. Procesar Reservas

```bash
python3 procesar_reservas.py archivo_reservas.csv
```

**Funciones:**
- ✅ Importa datos CSV a la pestaña "Ingresos 23 D MAYO"
- ✅ Distribuye todos los pasajeros a las grillas de PISO 1, 2 y 3
- ✅ Genera resumen estadístico en PISO 1 (columnas H-I, filas 278-282):
  - Total de Pasajeros
  - Total de Habitaciones Ocupadas
  - Total con Media Pensión/All Inclusive
- ✅ Crea backup automático con timestamp

### 2. Limpiar Grillas

```bash
python3 limpiar_grillas_pisos.py
```

**Funciones:**
- 🧹 Limpia todas las grillas de PISO 1, 2 y 3
- 🧹 Limpia la pestaña de Ingresos
- ✅ Preserva todos los encabezados
- 🗑️ Elimina automáticamente todos los archivos de backup
- ✅ Deja el archivo listo para nuevas reservas

## 📁 Archivos Principales

### Sistema de Consumos (Web App)

- **`app.py`** - Aplicación Flask principal (servidor web)
- **`templates/formulario.html`** - Interfaz web del sistema
- **`iniciar_recepcion.sh`** - Script de inicio automático
- **`consumos_diarios.csv`** - Base de datos de transacciones
- **`pasajeros.csv`** - Registro de huéspedes activos (validación)

### Scripts Python de Gestión de Reservas

- **`procesar_reservas.py`** - Script principal de procesamiento de reservas
- **`limpiar_grillas_pisos.py`** - Script de limpieza y reinicio de grillas

### Archivos de Datos

- **`Grilla de Pax 2030.xlsx`** - Archivo Excel principal con las grillas de trabajo
- **`datos_ficticios.csv`** - Datos de ejemplo para pruebas (sin información personal)

## 📊 Formato del CSV de Entrada

El archivo CSV debe contener las siguientes columnas:

```
Nro. habitación, Fecha de ingreso, Fecha de egreso, Plazas ocupadas, 
Tipo documento, Nro. doc., Apellido y nombre, Edad, Voucher, 
Servicios, Estado, Paquete, Sede
```

**Servicios soportados:**
- `DESAYUNO`
- `MEDIA PENSION` / `MEDIA PENSIÓN`
- `ALL INCLUSIVE`

## 🔄 Flujo de Trabajo Típico

1. **Limpiar grillas** (inicio de temporada o mes):
   ```bash
   python3 limpiar_grillas_pisos.py
   ```

2. **Procesar nuevas reservas**:
   ```bash
   python3 procesar_reservas.py reservas_enero.csv
   ```

3. **Agregar más reservas** (acumulativo):
   ```bash
   python3 procesar_reservas.py reservas_adicionales.csv
   ```

## 🔒 Seguridad y Backups

- ✅ **Backups automáticos**: Cada operación crea un backup con timestamp
- ✅ **Formato**: `BACKUP_YYYYMMDD_HHMMSS_Grilla de Pax 2030.xlsx`
- ✅ **Limpieza automática**: El script de limpieza elimina backups antiguos
- ⚠️ **Importante**: Cerrar el archivo Excel antes de ejecutar los scripts

## 📈 Estadísticas Generadas

El sistema calcula automáticamente:

- **Total Pasajeros**: Suma de todos los registros procesados
- **Total Habitaciones**: Cantidad de habitaciones únicas ocupadas
- **Total Media Pensión**: Pasajeros con servicio MAP o All Inclusive

Las estadísticas se actualizan en cada ejecución y se muestran en la pestaña PISO 1.

## 🛠️ Requisitos

```bash
Python 3.10+
Flask 3.x
pandas 2.x
openpyxl 3.1.5+
```

### Instalación de dependencias:

**Sistema de Consumos (recomendado usar entorno virtual):**
```bash
# El proyecto ya incluye un entorno virtual configurado en .venv/
# Si necesitas recrearlo:
python3 -m venv .venv
source .venv/bin/activate
pip install flask pandas openpyxl
```

**Sistema de Reservas:**
```bash
pip install openpyxl
```

## 📝 Notas Técnicas

- El script busca la primera fila vacía en Ingresos para agregar datos (acumulativo)
- Los encabezados se preservan siempre en la fila 1
- Las grillas de PISO usan columnas C-L para datos dinámicos
- El resumen se ubica en PISO 1, 5 filas después del texto "BEBIDAS" (fila 278)

## 🆕 Changelog

### v4.0 (06/01/2026) - Sistema de Consumos Web
- ➕ **NUEVO**: Aplicación web Flask para registro de consumos
- ➕ Formulario intuitivo con validación de habitaciones
- ➕ 3 categorías: Bebidas, Estadía, Map
- ➕ Generación de reportes Excel (salidas.xlsx) con columnas separadas
- ➕ Consulta diaria en CSV con tabla pivote
- ➕ Función de reinicio de temporada con backup automático
- ➕ Script de inicio con acceso directo desde escritorio
- ➕ Interfaz Bootstrap 5 responsive
- 🔒 Validación contra pasajeros.csv
- 📊 Historial completo de transacciones

### v3.0 (29/11/2025)
- ➕ Resumen estadístico en PISO 1 con 3 métricas
- ➕ Script de limpieza mejorado con preservación de encabezados
- ➕ Datos ficticios para pruebas seguras
- 🔧 Fix: Búsqueda correcta de primera fila vacía en Ingresos
- 🗑️ Eliminados: archivos ODS y test antiguos

### v2.0 (28/11/2025)
- ➕ Sistema unificado de importación + distribución
- ➕ Soporte dual Excel/ODS
- ➕ Backups automáticos con timestamp

## 📞 Soporte

Para consultas o reportar problemas, crear un issue en el repositorio.

---

## 🎯 Casos de Uso

**Sistema de Consumos**: Ideal para temporada alta (40+ habitaciones) cuando se necesita:
- Eliminar el procesamiento manual de comandas de papel
- Consolidar consumos de múltiples días antes del check-out
- Generar reportes de salida con formato específico (salidas.xlsx)

**Sistema de Reservas**: Gestión de ingresos y distribución de pasajeros en grillas por piso

---

**Desarrollado para la gestión hotelera - 2025/2026**
