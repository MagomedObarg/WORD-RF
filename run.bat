@echo off
REM Скрипт запуска AI Text Editor для Windows

echo ===================================
echo AI Text Editor - Starting...
echo ===================================

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python не найден. Пожалуйста, установите Python 3.8+
    echo   Скачайте с https://python.org
    pause
    exit /b 1
)

echo + Python найден
python --version

REM Проверка виртуального окружения
if not exist "venv\" (
    echo * Создание виртуального окружения...
    python -m venv venv
    
    if errorlevel 1 (
        echo X Ошибка создания виртуального окружения
        pause
        exit /b 1
    )
    
    echo + Виртуальное окружение создано
)

REM Активация виртуального окружения
echo * Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка/обновление зависимостей
echo * Проверка зависимостей...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo X Ошибка установки зависимостей
    pause
    exit /b 1
)

echo + Зависимости установлены

REM Проверка конфигурации
if not exist "config.ini" (
    echo ! config.ini не найден
    
    if exist "config.example.ini" (
        echo * Копирование config.example.ini в config.ini...
        copy config.example.ini config.ini
        echo ! ВАЖНО: Добавьте ваш Gemini API ключ в config.ini
        echo   Получите ключ на: https://ai.google.dev/
    ) else (
        echo X config.example.ini не найден
        pause
        exit /b 1
    )
)

REM Запуск приложения
echo.
echo ^ Запуск AI Text Editor...
echo ===================================
echo.
python main.py

REM Деактивация виртуального окружения при выходе
call venv\Scripts\deactivate.bat
