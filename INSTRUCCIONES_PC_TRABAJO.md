# 🏢 INSTRUCCIONES PARA PC DE TRABAJO

## 📋 Configuración Inicial en la PC del Trabajo

### 1️⃣ Clonar el Repositorio

```bash
# Abrir terminal en la carpeta deseada
cd /ruta/donde/quieras/el/proyecto

# Clonar repositorio
git clone git@github.com:xpablodaniel/recepcion2026-consumos.git

# O si usas HTTPS:
git clone https://github.com/xpablodaniel/recepcion2026-consumos.git

# Entrar al proyecto
cd recepcion2026-consumos
```

---

### 2️⃣ Verificar Branches Disponibles

```bash
# Ver todos los branches
git branch -a

# Deberías ver:
#   * main
#   remotes/origin/HEAD -> origin/main
#   remotes/origin/main
#   remotes/origin/temporada-activos
#   remotes/origin/temporada-jubilados
```

---

### 3️⃣ Configurar Entorno Python

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### 4️⃣ Preparar Datos Locales

**⚠️ IMPORTANTE:** Los archivos CSV con datos de pasajeros **NO están en el repositorio** por seguridad.

```bash
# Crear archivo de consumos vacío
echo "fecha,habitacion,pasajero,categoria,monto" > data/consumos_diarios.csv

# Crear carpeta de backups
mkdir -p data/backups
```

---

## 🔄 Uso Según Temporada

### 📅 Para Trabajadores ACTIVOS (Ene-Feb, Jun-Sep)

```bash
# 1. Cambiar a branch de activos
git checkout temporada-activos

# 2. Copiar CSV exportado del sistema de gestión
cp /ruta/al/archivo/consultaRegimenReport.csv data/

# 3. Procesar y cargar pasajeros
python3 cargar_trabajadores_activos.py

# 4. Verificar
head -2 data/pasajeros.csv

# 5. Iniciar servidor
python3 app.py

# 6. Abrir navegador en http://localhost:5000
```

**Características de esta temporada:**
- ✅ Check-out anticipado disponible
- ✅ Trabajan vienen por sus medios
- ✅ Media pensión o desayuno
- ✅ Pueden retirarse en cualquier momento

---

### 📅 Para Trabajadores JUBILADOS (Mar-May, Oct-Dic)

```bash
# 1. Cambiar a branch de jubilados
git checkout temporada-jubilados

# 2. Copiar CSV de jubilados
cp /ruta/al/archivo/jubilados.csv data/testJubis.csv

# 3. Cargar pasajeros
# Opción A: Si el CSV ya tiene el formato correcto
cp data/testJubis.csv data/pasajeros.csv

# Opción B: Si necesitas procesar el CSV
python3 gestionar_reservas_futuras.py  # O el script que uses

# 4. Verificar
head -2 data/pasajeros.csv

# 5. Iniciar servidor
python3 app.py

# 6. Abrir navegador en http://localhost:5000
```

**Características de esta temporada:**
- ❌ Sin check-out anticipado
- ✅ Traslado incluido (horarios fijos)
- ✅ Pensión completa
- ✅ Solo checkout el día programado
- ✅ Consumos individuales por pasajero

---

## 🔄 Cambio Rápido de Temporada

```bash
# Ver temporada actual
git branch

# Cambiar a activos (método rápido)
git checkout temporada-activos

# Cambiar a jubilados (método rápido)
git checkout temporada-jubilados

# Cambiar con script automático (hace backups)
./cambiar_temporada.sh activos
./cambiar_temporada.sh jubilados
```

---

## 📊 Comandos Útiles

### Verificar Estado

```bash
# Ver branch actual
git branch

# Contar pasajeros cargados
wc -l data/pasajeros.csv

# Ver primer pasajero
head -2 data/pasajeros.csv | tail -1

# Ver si hay checkout anticipado (activos)
grep -c "Check-out Anticipado" templates/ficha_habitacion.html
# 0 = Jubilados, >0 = Activos
```

### Actualizar Código desde GitHub

```bash
# Siempre desde el branch que estés usando
git pull origin temporada-activos   # Si estás en activos
git pull origin temporada-jubilados # Si estás en jubilados
```

### Backup de Datos

```bash
# Backup manual de datos
cp data/pasajeros.csv data/backups/pasajeros_backup_$(date +%Y%m%d).csv
cp data/consumos_diarios.csv data/backups/consumos_backup_$(date +%Y%m%d).csv
```

---

## 🔒 Seguridad - IMPORTANTE

### ❌ NUNCA HAGAS ESTO:

```bash
# ❌ NO hacer git add de archivos CSV con datos reales
git add data/pasajeros.csv          # ❌ NUNCA
git add data/consultaRegimenReport.csv  # ❌ NUNCA
git add data/testJubis.csv          # ❌ NUNCA

# ❌ NO hacer commit de datos sensibles
git commit -m "Agregando pasajeros"  # ❌ SOLO si son datos de ejemplo
```

### ✅ SIEMPRE VERIFICA:

```bash
# Antes de cualquier commit, verificar qué vas a subir
git status

# Si aparece data/pasajeros.csv u otros CSV, NO hacer commit
# Solo deberían aparecer archivos de código (.py, .html, .md, .sh)
```

---

## 🆘 Solución de Problemas

### Error: "KeyError: 'Fecha de ingreso'"

**Causa:** El CSV de pasajeros tiene nombres de columnas incorrectos.

**Solución:**
```bash
# Para trabajadores activos
python3 cargar_trabajadores_activos.py

# Verificar que las columnas sean correctas
head -1 data/pasajeros.csv
# Debe incluir: "Apellido y nombre,Nro. doc.,Edad,Nro. habitación,Fecha de ingreso,Fecha de egreso..."
```

### Error: "Port 5000 is in use"

**Causa:** Ya hay un servidor Flask corriendo.

**Solución:**
```bash
# Opción 1: Matar proceso anterior
pkill -f "python.*app.py"

# Opción 2: Usar otro puerto
python3 app.py --port 5001
```

### No veo checkout anticipado (debería aparecer en temporada activos)

**Causa:** Estás en el branch incorrecto.

**Solución:**
```bash
# Verificar branch
git branch

# Si no estás en temporada-activos, cambiar
git checkout temporada-activos

# Recargar navegador (F5)
```

---

## 📅 Calendario de Temporadas

| Mes | Temporada | Branch | Comando |
|-----|-----------|--------|---------|
| Enero | Activos | `temporada-activos` | `git checkout temporada-activos` |
| Febrero | Activos | `temporada-activos` | `git checkout temporada-activos` |
| **Marzo** | **Jubilados** | `temporada-jubilados` | `git checkout temporada-jubilados` |
| Abril | Jubilados | `temporada-jubilados` | `git checkout temporada-jubilados` |
| Mayo | Jubilados | `temporada-jubilados` | `git checkout temporada-jubilados` |
| Junio | Activos | `temporada-activos` | `git checkout temporada-activos` |
| Julio | Activos | `temporada-activos` | `git checkout temporada-activos` |
| Agosto | Activos | `temporada-activos` | `git checkout temporada-activos` |
| Septiembre | Activos | `temporada-activos` | `git checkout temporada-activos` |
| Octubre | Jubilados | `temporada-jubilados` | `git checkout temporada-jubilados` |
| Noviembre | Jubilados | `temporada-jubilados` | `git checkout temporada-jubilados` |
| Diciembre | Jubilados | `temporada-jubilados` | `git checkout temporada-jubilados` |

---

## 📚 Documentación Adicional

Consulta estos archivos para más información:

- **[README.md](README.md)** - Descripción general del proyecto
- **[data/README.md](data/README.md)** - Instrucciones sobre archivos de datos
- **[GUIA_CAMBIO_TEMPORADA.md](GUIA_CAMBIO_TEMPORADA.md)** - Guía completa de cambio de temporada
- **[REFERENCIA_RAPIDA_TEMPORADAS.md](REFERENCIA_RAPIDA_TEMPORADAS.md)** - Comandos rápidos
- **[EJEMPLOS_USO_TEMPORADAS.md](EJEMPLOS_USO_TEMPORADAS.md)** - 10 escenarios comunes

---

## ✅ Checklist de Inicio de Temporada

- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Branch correcto seleccionado (activos o jubilados)
- [ ] Archivo `data/consumos_diarios.csv` creado
- [ ] CSV de pasajeros cargado en `data/pasajeros.csv`
- [ ] Servidor funcionando (`python3 app.py`)
- [ ] Dashboard accesible en navegador

---

**Repositorio:** https://github.com/xpablodaniel/recepcion2026-consumos  
**Última actualización:** 1 de Marzo 2026
