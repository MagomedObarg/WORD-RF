#!/bin/bash
# Скрипт запуска AI Text Editor для Linux/macOS

echo "==================================="
echo "AI Text Editor - Starting..."
echo "==================================="

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Пожалуйста, установите Python 3.8+"
    exit 1
fi

echo "✓ Python найден: $(python3 --version)"

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "⚙️ Создание виртуального окружения..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Ошибка создания виртуального окружения"
        exit 1
    fi
    
    echo "✓ Виртуальное окружение создано"
fi

# Активация виртуального окружения
echo "⚙️ Активация виртуального окружения..."
source venv/bin/activate

# Проверка зависимостей
if [ ! -f "venv/bin/pip" ]; then
    echo "❌ pip не найден в виртуальном окружении"
    exit 1
fi

# Установка/обновление зависимостей
echo "⚙️ Проверка зависимостей..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Ошибка установки зависимостей"
    exit 1
fi

echo "✓ Зависимости установлены"

# Проверка конфигурации
if [ ! -f "config.ini" ]; then
    echo "⚠️ config.ini не найден"
    
    if [ -f "config.example.ini" ]; then
        echo "⚙️ Копирование config.example.ini в config.ini..."
        cp config.example.ini config.ini
        echo "⚠️ ВАЖНО: Добавьте ваш Gemini API ключ в config.ini"
        echo "   Получите ключ на: https://ai.google.dev/"
    else
        echo "❌ config.example.ini не найден"
        exit 1
    fi
fi

# Запуск приложения
echo ""
echo "🚀 Запуск AI Text Editor..."
echo "==================================="
echo ""
python3 main.py

# Деактивация виртуального окружения при выходе
deactivate
