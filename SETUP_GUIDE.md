# 🚀 Подробное руководство по установке

## Содержание
- [Системные требования](#системные-требования)
- [Установка на Windows](#установка-на-windows)
- [Установка на macOS](#установка-на-macos)
- [Установка на Linux](#установка-на-linux)
- [Получение API ключа](#получение-api-ключа)
- [Решение проблем](#решение-проблем)

## Системные требования

### Минимальные требования
- **ОС**: Windows 10+, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 или выше
- **RAM**: 2 GB
- **Диск**: 500 MB свободного места
- **Интернет**: для работы AI-функций

### Рекомендуемые требования
- **ОС**: Windows 11, macOS 12+, Linux (Ubuntu 22.04+)
- **Python**: 3.10 или выше
- **RAM**: 4 GB или больше
- **Диск**: 1 GB свободного места
- **Интернет**: стабильное подключение >1 Мбит/с

## Установка на Windows

### Шаг 1: Установка Python

1. Скачайте Python с [python.org](https://www.python.org/downloads/)
2. Запустите установщик
3. ✅ **ВАЖНО**: Отметьте "Add Python to PATH"
4. Нажмите "Install Now"

Проверка установки:
```cmd
python --version
```

Должно вывести: `Python 3.x.x`

### Шаг 2: Загрузка проекта

**Вариант A: Через Git**
```cmd
git clone https://github.com/your-username/ai-text-editor.git
cd ai-text-editor
```

**Вариант B: Скачать ZIP**
1. Скачайте ZIP с GitHub
2. Распакуйте в удобное место
3. Откройте командную строку в этой папке

### Шаг 3: Создание виртуального окружения

```cmd
python -m venv venv
venv\Scripts\activate
```

После активации должно появиться `(venv)` в начале строки.

### Шаг 4: Установка зависимостей

```cmd
pip install -r requirements.txt
```

### Шаг 5: Настройка API ключа

1. Откройте `config.ini` в Notepad
2. Замените `YOUR_GEMINI_API_KEY_HERE` на ваш ключ
3. Сохраните файл

### Шаг 6: Запуск

```cmd
python main.py
```

## Установка на macOS

### Шаг 1: Установка Python

macOS обычно имеет Python 2.7, нужен Python 3.

**Через Homebrew (рекомендуется):**
```bash
# Установка Homebrew (если еще не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка Python
brew install python@3.11
```

**Или скачайте с [python.org](https://www.python.org/downloads/)**

Проверка:
```bash
python3 --version
```

### Шаг 2: Загрузка проекта

```bash
git clone https://github.com/your-username/ai-text-editor.git
cd ai-text-editor
```

### Шаг 3: Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 4: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 5: Настройка API ключа

```bash
nano config.ini
# или
open -e config.ini
```

Замените ключ, сохраните (Ctrl+O, Enter, Ctrl+X для nano).

### Шаг 6: Запуск

```bash
python main.py
```

## Установка на Linux

### Шаг 1: Установка Python и зависимостей

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk
```

Проверка:
```bash
python3 --version
```

### Шаг 2: Загрузка проекта

```bash
git clone https://github.com/your-username/ai-text-editor.git
cd ai-text-editor
```

### Шаг 3: Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 4: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 5: Настройка API ключа

```bash
nano config.ini
```

Замените ключ, сохраните (Ctrl+O, Enter, Ctrl+X).

### Шаг 6: Запуск

```bash
python main.py
```

## Получение API ключа

### Подробная инструкция

1. **Перейдите на Google AI Studio**
   - Откройте [https://ai.google.dev/](https://ai.google.dev/)
   - Или [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. **Войдите в аккаунт Google**
   - Используйте существующий аккаунт
   - Или создайте новый

3. **Примите условия использования**
   - Прочитайте и примите Terms of Service
   - Подтвердите согласие

4. **Создайте API ключ**
   - Нажмите "Get API Key" или "Create API Key"
   - Выберите "Create API key in new project"
   - Или выберите существующий Google Cloud проект

5. **Скопируйте ключ**
   - ⚠️ **ВАЖНО**: Скопируйте ключ сразу
   - Он будет показан только один раз
   - Сохраните в надежном месте

6. **Добавьте в config.ini**
   ```ini
   [API]
   gemini_api_key = AIzaSy...ваш_ключ_здесь...
   ```

### Лимиты бесплатного использования

**Gemini API Free Tier (актуально на 2024):**
- 60 запросов в минуту
- 1,500 запросов в день
- Бесплатно для личного использования

**Если нужно больше:**
- Перейдите на платный план в Google Cloud
- Стоимость: ~$0.001 за 1000 символов

### Безопасность API ключа

✅ **Делайте:**
- Храните ключ в config.ini (он в .gitignore)
- Используйте переменные окружения для продакшена
- Регулярно обновляйте ключи

❌ **Не делайте:**
- Не коммитьте ключ в Git
- Не публикуйте в открытых репозиториях
- Не передавайте третьим лицам

## Решение проблем

### Python не найден

**Windows:**
```cmd
# Проверьте, установлен ли Python
where python

# Если не найден, переустановите с галочкой "Add to PATH"
```

**macOS/Linux:**
```bash
# Используйте python3 вместо python
which python3
```

### Ошибка при установке пакетов

**Проблема:** `pip install` выдает ошибки

**Решение 1:** Обновите pip
```bash
python -m pip install --upgrade pip
```

**Решение 2:** Установите с правами администратора
```bash
# Windows (от администратора)
pip install -r requirements.txt

# macOS/Linux
sudo pip install -r requirements.txt
```

**Решение 3:** Используйте virtualenv
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

### CustomTkinter не работает

**Симптомы:** Окно не открывается или ошибки с Tkinter

**Решение для Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Решение для macOS:**
```bash
brew install python-tk@3.11
```

### AI не отвечает

**Проблема 1:** "AI не настроен"
- Проверьте, что API ключ добавлен в config.ini
- Перезапустите приложение

**Проблема 2:** "API Error: 429"
- Превышен лимит запросов
- Подождите минуту и попробуйте снова

**Проблема 3:** "API Error: 401"
- Неверный API ключ
- Получите новый ключ на ai.google.dev

**Проблема 4:** "Connection error"
- Проверьте интернет-соединение
- Проверьте, что ai.google.dev доступен
- Отключите VPN/прокси (если используете)

### Проблемы с открытием .docx

**Ошибка:** "Cannot open .docx file"

**Решение:**
```bash
pip install --upgrade python-docx
```

Если не помогло:
```bash
pip uninstall python-docx
pip install python-docx
```

### Проблемы с PDF экспортом

**Ошибка:** "PDF export failed"

**Решение:**
```bash
pip install --upgrade reportlab
```

**Для поддержки Unicode:**
```bash
# Установите дополнительные шрифты
pip install reportlab-fonttools
```

### Приложение зависает

**Возможные причины:**
1. Долгий AI запрос (подождите 10-30 секунд)
2. Большой документ (>10,000 слов)
3. Недостаточно RAM

**Решения:**
- Разбейте документ на части
- Закройте другие приложения
- Перезапустите приложение

## Обновление

### Обновление приложения

```bash
# Получите последнюю версию
git pull origin main

# Обновите зависимости
pip install --upgrade -r requirements.txt
```

### Обновление Python

1. Скачайте новую версию Python
2. Установите
3. Пересоздайте виртуальное окружение:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Создание standalone исполняемого файла

### Используя PyInstaller

```bash
# Установите PyInstaller
pip install pyinstaller

# Создайте .exe (Windows) или app (macOS)
pyinstaller --onefile --windowed --name="AI Text Editor" main.py

# Результат будет в папке dist/
```

### Используя cx_Freeze

```bash
# Установите cx_Freeze
pip install cx_Freeze

# Создайте setup.py
# Затем запустите
python setup.py build
```

## Автозапуск при загрузке системы

### Windows

1. Создайте ярлык для `main.py`
2. Нажмите `Win+R`, введите `shell:startup`
3. Скопируйте ярлык в открывшуюся папку

### macOS

1. Откройте "System Preferences" → "Users & Groups"
2. Выберите свой аккаунт → "Login Items"
3. Нажмите "+" и добавьте приложение

### Linux (systemd)

```bash
# Создайте service файл
nano ~/.config/systemd/user/ai-text-editor.service

# Добавьте:
[Unit]
Description=AI Text Editor

[Service]
ExecStart=/path/to/venv/bin/python /path/to/main.py

[Install]
WantedBy=default.target

# Включите службу
systemctl --user enable ai-text-editor
systemctl --user start ai-text-editor
```

## Дополнительная настройка

### Изменение темы

В `config.ini`:
```ini
[EDITOR]
theme = dark  # или light
```

### Настройка автосохранения

```ini
[EDITOR]
autosave_interval = 120  # секунды (120 = 2 минуты)
```

### Настройка AI параметров

```ini
[AI_SETTINGS]
temperature = 0.5  # Более консервативные ответы (0.0-1.0)
max_tokens = 4096  # Больше максимальная длина ответа
```

## Полезные команды

### Проверка версий
```bash
python --version
pip --version
pip list  # Все установленные пакеты
```

### Очистка кэша
```bash
pip cache purge
python -m pip cache purge
```

### Переустановка всех зависимостей
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## Контакты для поддержки

Если проблема не решена:
1. Проверьте [Issues на GitHub](https://github.com/your-username/ai-text-editor/issues)
2. Создайте новый Issue с описанием проблемы
3. Приложите:
   - Версию Python (`python --version`)
   - Операционную систему
   - Текст ошибки
   - Шаги для воспроизведения

---

**Успешной установки! 🚀**
