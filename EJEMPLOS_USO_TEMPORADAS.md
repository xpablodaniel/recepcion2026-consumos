# 🔄 EJEMPLOS DE USO - Sistema de Cambio de Temporada

## 🎯 Escenarios Comunes

---

### 📅 Escenario 1: Estamos en Marzo (Temporada de Jubilados)

**Tu situación:** Es Marzo 2026, comienza la temporada de jubilados.

**Lo que debes hacer:**

```bash
# 1. Cambiar a temporada jubilados
./cambiar_temporada.sh jubilados

# O manualmente:
git checkout temporada-jubilados

# 2. Cargar CSV de jubilados
# Reemplazar data/pasajeros.csv con tu archivo de jubilados
# O usar el script de carga

# 3. Verificar
python app.py
# Abrir navegador en http://localhost:5000
```

**Qué verás:**
- ❌ NO aparece módulo de checkout anticipado
- ✅ Solo mensaje de checkout cuando es el día programado
- ✅ Mensaje: "El huésped tiene traslado incluido"

---

### 📅 Escenario 2: Estamos en Junio (Temporada de Activos)

**Tu situación:** Es Junio 2026, comienza la temporada de trabajadores activos.

**Lo que debes hacer:**

```bash
# 1. Cambiar a temporada activos
./cambiar_temporada.sh activos

# O manualmente:
git checkout temporada-activos

# 2. Cargar CSV de trabajadores activos
# Reemplazar data/consultaRegimenReport.csv con el nuevo archivo
python3 cargar_trabajadores_activos.py

# 3. Verificar
python app.py
```

**Qué verás:**
- ✅ Aparece módulo de checkout anticipado (alerta amarilla)
- ✅ Mensaje: "Los trabajadores activos vienen por sus medios"
- ✅ Botón "Procesar Check-out Anticipado" siempre visible

---

### 🔍 Escenario 3: Verificar en qué temporada estoy

**Tu situación:** No recuerdas en qué temporada estás trabajando.

**Lo que debes hacer:**

```bash
# Ver branch actual
git branch

# Resultado ejemplo:
#   main
# * temporada-activos      ← El asterisco indica el activo
#   temporada-jubilados
```

**También puedes verificar los datos:**

```bash
# Contar pasajeros
wc -l data/pasajeros.csv

# Si muestra ~45 líneas → JUBILADOS (44 pasajeros)
# Si muestra ~22 líneas → ACTIVOS (21 pasajeros)
```

---

### 🚨 Escenario 4: Me equivoqué de temporada

**Tu situación:** Abriste el dashboard y te diste cuenta que estás en la temporada incorrecta.

**Lo que debes hacer:**

```bash
# Si agregaste consumos por error, simplemente cambia de temporada
# Los consumos están separados por branch

# Cambiar a la temporada correcta
./cambiar_temporada.sh [activos|jubilados]

# Git automáticamente restaurará los datos correctos
```

**No te preocupes:** Cada temporada tiene su propio archivo de consumos. Los cambios no se mezclan.

---

### 💾 Escenario 5: Hacer backup antes de cambiar temporada

**Tu situación:** Quieres guardar el estado actual antes de cambiar.

**Lo que debes hacer:**

```bash
# El script cambiar_temporada.sh YA hace backup automático
# Pero si quieres uno manual:

# 1. Backup manual
cp data/pasajeros.csv data/backups/pasajeros_backup_$(date +%Y%m%d).csv
cp data/consumos_diarios.csv data/backups/consumos_backup_$(date +%Y%m%d).csv

# 2. Commit de cambios pendientes
git add .
git commit -m "Guardado antes de cambiar temporada"

# 3. Ahora sí, cambiar
./cambiar_temporada.sh [activos|jubilados]
```

---

### 🔄 Escenario 6: Cambiar varias veces en un día (pruebas)

**Tu situación:** Estás probando el sistema y quieres cambiar entre temporadas varias veces.

**Lo que debes hacer:**

```bash
# Cambio rápido SIN script automático
git checkout temporada-activos    # Ir a activos
git checkout temporada-jubilados   # Ir a jubilados
git checkout temporada-activos     # Volver a activos

# Git cambia TODO automáticamente:
# - Templates (con/sin checkout anticipado)
# - Datos de pasajeros
# - Consumos
```

**Ventaja:** Es instantáneo, no necesitas recargar nada manualmente.

---

### 📊 Escenario 7: Ver diferencias entre temporadas

**Tu situación:** Quieres ver exactamente qué cambia entre una temporada y otra.

**Lo que debes hacer:**

```bash
# Ver diferencias en templates
git diff temporada-activos temporada-jubilados templates/

# Ver diferencias en datos
git diff temporada-activos temporada-jubilados data/pasajeros.csv

# Ver resumen de commits
git log --oneline --graph --all
```

---

### 🛠️ Escenario 8: Agregar funcionalidad a UNA sola temporada

**Tu situación:** Quieres agregar una nueva funcionalidad solo para jubilados, no para activos.

**Lo que debes hacer:**

```bash
# 1. Ir a la temporada específica
git checkout temporada-jubilados

# 2. Hacer los cambios (editar archivos)
# Por ejemplo: agregar validación especial para pensión completa

# 3. Guardar cambios SOLO en ese branch
git add .
git commit -m "Nueva funcionalidad solo para jubilados"

# 4. Verificar que la otra temporada NO tiene el cambio
git checkout temporada-activos
# El cambio NO estará aquí ✅
```

**Importante:** Los branches son independientes. Los cambios en uno NO afectan al otro.

---

### 📅 Escenario 9: Inicio de nueva temporada con datos frescos

**Tu situación:** Es Octubre 2026, empieza nueva temporada de jubilados con nuevos pasajeros.

**Lo que debes hacer:**

```bash
# 1. Cambiar a temporada jubilados
./cambiar_temporada.sh jubilados

# 2. El script automáticamente:
#    ✅ Hace backup de datos actuales
#    ✅ Limpia consumos_diarios.csv
#    ✅ Cambia al branch correcto

# 3. Cargar nuevo CSV de jubilados
# Copiar tu nuevo archivo a data/pasajeros.csv
# O procesarlo con un script

# 4. Verificar
python app.py
```

---

### 🔍 Escenario 10: Recuperar datos de temporada anterior

**Tu situación:** Estás en Octubre (jubilados) pero necesitas consultar datos de la última temporada de activos (Septiembre).

**Lo que debes hacer:**

```bash
# 1. Ver en qué branch estás
git branch
# * temporada-jubilados  ← Estás aquí

# 2. Cambiar temporalmente a activos para consultar
git checkout temporada-activos

# 3. Verificar datos
cat data/pasajeros.csv
# O abrir dashboard para ver consumos históricos

# 4. Volver a jubilados cuando termines
git checkout temporada-jubilados
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS

| Acción | Comando |
|--------|---------|
| Ver temporada actual | `git branch` |
| Cambiar a activos | `./cambiar_temporada.sh activos` |
| Cambiar a jubilados | `./cambiar_temporada.sh jubilados` |
| Cambio rápido manual | `git checkout temporada-[activos\|jubilados]` |
| Ver diferencias | `git diff temporada-activos temporada-jubilados` |
| Backup manual | `cp data/pasajeros.csv data/backups/pasajeros_$(date +%Y%m%d).csv` |
| Ver commits | `git log --oneline --all` |
| Contar pasajeros | `wc -l data/pasajeros.csv` |

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### ❌ Error: "No se puede cambiar, hay cambios sin guardar"

**Solución:**
```bash
git add .
git commit -m "Guardado rápido"
./cambiar_temporada.sh [temporada]
```

### ❌ Error: "El script no tiene permisos de ejecución"

**Solución:**
```bash
chmod +x cambiar_temporada.sh
./cambiar_temporada.sh [temporada]
```

### ❌ Error: "Aparece checkout anticipado en jubilados"

**Solución:**
```bash
# Verificar que estás en el branch correcto
git branch

# Si estás en temporada-jubilados y ves checkout anticipado:
git log --oneline -5
# Buscar si hay commits incorrectos

# Cambiar a temporada-activos si era un error
git checkout temporada-activos
```

---

**Última actualización:** 1 de Marzo 2026  
**Versión:** 1.0  
**Estado:** ✅ Todos los escenarios probados y funcionando
