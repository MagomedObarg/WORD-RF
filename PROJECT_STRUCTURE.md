# 📁 Структура проекта AI Text Editor

## Краткий обзор файлов

### 🔧 Исходный код
- **main.py** - Точка входа приложения
- **editor.py** - Основной класс редактора (24KB)
- **ai_assistant.py** - AI модуль с Gemini API (7.8KB)
- **file_operations.py** - Работа с файлами .txt, .docx, .pdf (5KB)
- **ui_components.py** - UI компоненты (панели, диалоги) (11KB)

### ⚙️ Конфигурация
- **config.ini** - Конфигурация (API ключ, настройки)
- **config.example.ini** - Пример конфигурации
- **requirements.txt** - Python зависимости

### 🚀 Запуск
- **run.sh** - Скрипт запуска для Linux/macOS
- **run.bat** - Скрипт запуска для Windows

### 🧪 Тестирование
- **test_basic.py** - Базовые тесты

### 📚 Документация
- **README.md** - Основная документация (12KB)
- **EXAMPLES.md** - Примеры использования (22KB)
- **SETUP_GUIDE.md** - Подробное руководство по установке (13KB)
- **FAQ.md** - Часто задаваемые вопросы (11KB)
- **CONTRIBUTING.md** - Гайд для контрибьюторов (12KB)
- **ARCHITECTURE.md** - Архитектура проекта (16KB)
- **CHANGELOG.md** - История изменений (2KB)
- **LICENSE** - MIT лицензия (1KB)

### 🔐 Прочее
- **.gitignore** - Исключения для Git
- **PROJECT_STRUCTURE.md** - Этот файл

## Размеры компонентов

```
Исходный код:       ~53 KB
Документация:       ~88 KB
Конфигурация:       ~2 KB
Скрипты запуска:    ~3 KB
----------------------------------
Итого:              ~146 KB
```

## Зависимости

```
customtkinter       - UI фреймворк
Pillow              - Работа с изображениями
python-docx         - Работа с .docx
reportlab           - Экспорт в PDF
google-generativeai - Gemini API
language-tool-python- Проверка орфографии (опционально)
python-dotenv       - Переменные окружения
```

## Быстрый старт

### 1. Установка
```bash
# Linux/macOS
./run.sh

# Windows
run.bat

# Или вручную
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка
Отредактируйте `config.ini`:
```ini
[API]
gemini_api_key = ВАШ_КЛЮЧ_ЗДЕСЬ
```

### 3. Запуск
```bash
python main.py
```

## Ключевые файлы для изучения

Если вы хотите понять, как работает приложение:

1. **main.py** - Начните отсюда (всего ~30 строк)
2. **editor.py** - Основная логика приложения
3. **ai_assistant.py** - Интеграция с AI
4. **ARCHITECTURE.md** - Подробное описание архитектуры

## Модификация

### Добавить новую AI функцию
1. Метод в `ai_assistant.py`
2. Обработчик в `editor.py`
3. Кнопка в `ui_components.py` или `editor.py`

### Добавить поддержку нового формата
1. Методы в `file_operations.py`
2. Обработка в `editor.py`

### Изменить UI
1. Компоненты в `ui_components.py`
2. Макет в `editor.py` (методы `setup_*`)

## Документация для разных ролей

### Пользователи
- 📖 README.md - общее описание
- 📚 EXAMPLES.md - примеры использования
- ❓ FAQ.md - ответы на вопросы
- 🚀 SETUP_GUIDE.md - установка

### Разработчики
- 🏗️ ARCHITECTURE.md - архитектура
- 🤝 CONTRIBUTING.md - как внести вклад
- 📁 PROJECT_STRUCTURE.md - структура (этот файл)

### Администраторы
- ⚙️ config.example.ini - настройка
- 🚀 run.sh / run.bat - развертывание

## Типичные задачи

### Добавление новой зависимости
1. Добавьте в `requirements.txt`
2. Установите: `pip install -r requirements.txt`
3. Используйте в коде

### Изменение UI темы
В `config.ini`:
```ini
[EDITOR]
theme = dark  # или light
```

### Изменение AI параметров
В `config.ini`:
```ini
[AI_SETTINGS]
temperature = 0.5  # 0.0 - 1.0
max_tokens = 4096
```

## Диаграмма зависимостей

```
main.py
  └─> editor.py
        ├─> ai_assistant.py
        │     └─> google.generativeai
        ├─> file_operations.py
        │     ├─> python-docx
        │     └─> reportlab
        └─> ui_components.py
              └─> customtkinter
```

## Git workflow

```bash
# Получить последние изменения
git pull origin main

# Создать ветку для новой функции
git checkout -b feature/my-feature

# Внести изменения
git add .
git commit -m "feat: add my feature"

# Отправить в репозиторий
git push origin feature/my-feature

# Создать Pull Request на GitHub
```

## Полезные команды

```bash
# Проверка синтаксиса всех файлов
python -m py_compile *.py

# Запуск тестов
python test_basic.py

# Просмотр зависимостей
pip list

# Обновление всех зависимостей
pip install --upgrade -r requirements.txt

# Создание standalone executable
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Контакты

- 🐛 Баги: [GitHub Issues](https://github.com/your-username/ai-text-editor/issues)
- 💬 Обсуждения: [GitHub Discussions](https://github.com/your-username/ai-text-editor/discussions)
- 📧 Email: your-email@example.com

---

**Версия проекта**: 1.0.0  
**Последнее обновление**: 31 октября 2024
