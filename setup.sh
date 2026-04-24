#!/bin/bash

echo "🚀 Configurando API REST Flask + Cliente TypeScript"
echo "=================================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    echo "📥 Instala Node.js desde: https://nodejs.org/"
    exit 1
fi

echo "✅ Python 3 y Node.js detectados"

# Backend setup
echo ""
echo "🐍 Configurando Backend (Flask)..."
echo "================================="

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias Python..."
pip3 install -r requirements.txt

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python3 init_db.py

echo "✅ Backend configurado correctamente"

# Frontend setup
echo ""
echo "💻 Configurando Frontend (TypeScript)..."
echo "======================================="

cd client

# Instalar dependencias
echo "📥 Instalando dependencias Node.js..."
npm install

echo "✅ Frontend configurado correctamente"

cd ..

echo ""
echo "🎉 ¡Configuración completada!"
echo "============================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣ Iniciar el backend:"
echo "   python3 run.py"
echo ""
echo "2️⃣ En otra terminal, iniciar el frontend:"
echo "   cd client && npm run dev"
echo ""
echo "3️⃣ Abrir en el navegador:"
echo "   http://localhost:3000"
echo ""
echo "📚 Documentación completa en README.md"
echo ""
echo "🚀 ¡Feliz desarrollo!"