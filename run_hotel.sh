#!/bin/bash
# Script automatizado para iniciar el sistema de recepción del hotel
# Compatible con Ubuntu nativo

# Obtener la ruta absoluta del proyecto
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "🏨 Sistema de Gestión Hotelera - Recepción 2026"
echo "================================================"
echo ""

# 1. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "⚙️  Configurando entorno virtual por primera vez..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado"
    echo ""
fi

# 2. Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# 3. Instalar/actualizar dependencias
echo "📦 Verificando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✅ Dependencias actualizadas"
echo ""

# 4. Abrir el navegador automáticamente
# Espera 3 segundos para que Flask inicie correctamente
echo "🌐 Abriendo navegador en 3 segundos..."
(sleep 3 && xdg-open http://127.0.0.1:5000 2>/dev/null) &

# 5. Ejecutar la aplicación Flask
echo "🚀 Iniciando servidor Flask..."
echo "================================================"
echo ""
echo "✅ Servidor iniciado correctamente"
echo "🌐 Accede desde tu navegador a: http://localhost:5000"
echo ""
echo "⚠️  NO CIERRES ESTA VENTANA mientras uses el sistema"
echo "⚠️  Para detener el servidor: presiona Ctrl+C"
echo ""
echo "================================================"
echo ""

python3 app.py
