# 🏗️ Архитектура AI Text Editor

## Обзор

AI Text Editor построен на модульной архитектуре с четким разделением ответственности. Проект следует паттерну MVC (Model-View-Controller) адаптированному для desktop приложения.

## Структура проекта

```
ai-text-editor/
│
├── main.py                 # Точка входа, инициализация приложения
├── editor.py               # Основной класс редактора (Controller + View)
├── ai_assistant.py         # AI-модуль, интеграция с Gemini (Model)
├── file_operations.py      # Работа с файлами (Model)
├── ui_components.py        # UI компоненты (View)
│
├── config.ini              # Конфигурация (не в Git)
├── config.example.ini      # Пример конфигурации
├── requirements.txt        # Python зависимости
│
├── run.sh                  # Запуск для Linux/macOS
├── run.bat                 # Запуск для Windows
├── test_basic.py           # Базовые тесты
│
├── README.md               # Основная документация
├── EXAMPLES.md             # Примеры использования
├── SETUP_GUIDE.md          # Руководство по установке
├── FAQ.md                  # Часто задаваемые вопросы
├── CONTRIBUTING.md         # Гайд для контрибьюторов
├── CHANGELOG.md            # История изменений
├── ARCHITECTURE.md         # Этот файл
├── LICENSE                 # MIT лицензия
│
└── .gitignore              # Исключения для Git
```

## Компоненты

### 1. main.py
**Назначение**: Точка входа приложения

**Ответственность**:
- Инициализация логирования
- Создание экземпляра TextEditor
- Запуск главного цикла событий
- Обработка критических ошибок

**Зависимости**: 
- `editor.py`

**Код**:
```python
def main():
    logger.info("Starting AI Text Editor")
    app = TextEditor()
    app.mainloop()
```

### 2. editor.py
**Назначение**: Основной класс редактора (Controller + View)

**Ответственность**:
- Управление UI приложения
- Координация между компонентами
- Обработка пользовательского ввода
- Управление состоянием документа
- Связь с AI-ассистентом
- Файловые операции

**Ключевые методы**:
```python
class TextEditor(ctk.CTk):
    def __init__(self)                  # Инициализация
    def load_config(self)               # Загрузка конфигурации
    def setup_ui(self)                  # Построение интерфейса
    def setup_bindings(self)            # Горячие клавиши
    
    # Файловые операции
    def new_file(self)
    def open_file(self)
    def save_file(self)
    def export_pdf(self)
    
    # AI функции
    def ai_action(self, action: str)
    def handle_ai_response(self, response: str, error: Optional[str])
    
    # UI управление
    def toggle_ai_panel(self)
    def show_file_menu(self)
    def show_ai_menu(self)
```

**Паттерны**:
- **Observer**: Реагирует на события UI
- **Mediator**: Координирует взаимодействие компонентов
- **Command**: Обработка пользовательских действий

### 3. ai_assistant.py
**Назначение**: Интеграция с Google Gemini API (Model)

**Ответственность**:
- Управление подключением к Gemini API
- Асинхронная отправка запросов
- Обработка ответов и ошибок
- Кэширование (в будущем)
- История диалогов

**Ключевые методы**:
```python
class AIAssistant:
    def __init__(self, api_key: str, model_name: str, temperature: float)
    def is_ready(self) -> bool
    
    # Базовая генерация
    def generate_async(self, prompt: str, callback: Callable)
    
    # Специализированные функции
    def improve_text(self, text: str, callback: Callable)
    def rewrite_text(self, text: str, style: str, callback: Callable)
    def continue_text(self, text: str, callback: Callable)
    def fix_grammar(self, text: str, callback: Callable)
    def shorten_text(self, text: str, callback: Callable)
    def expand_text(self, text: str, callback: Callable)
    def translate_text(self, text: str, target_lang: str, callback: Callable)
    def summarize_text(self, text: str, callback: Callable)
    def generate_document(self, doc_type: str, desc: str, callback: Callable)
    def answer_question(self, question: str, context: str, callback: Callable)
    def chat(self, message: str, callback: Callable)
    
    # История
    def get_chat_history(self) -> list
    def clear_history(self)
```

**Паттерны**:
- **Facade**: Упрощает работу с Gemini API
- **Strategy**: Различные стратегии генерации текста
- **Callback**: Асинхронная обработка через callback функции

**Асинхронность**:
```python
def generate_async(self, prompt: str, callback: Callable):
    def task():
        response = self.model.generate_content(prompt)
        callback(response.text, None)
    
    thread = threading.Thread(target=task, daemon=True)
    thread.start()
```

### 4. file_operations.py
**Назначение**: Работа с файлами (Model)

**Ответственность**:
- Открытие/сохранение .txt файлов
- Открытие/сохранение .docx файлов
- Экспорт в PDF
- Валидация путей файлов

**Ключевые методы**:
```python
class FileOperations:
    @staticmethod
    def new_document() -> str
    
    @staticmethod
    def open_txt(filepath: str) -> str
    
    @staticmethod
    def open_docx(filepath: str) -> str
    
    @staticmethod
    def save_txt(filepath: str, content: str)
    
    @staticmethod
    def save_docx(filepath: str, content: str, formatting: dict)
    
    @staticmethod
    def export_pdf(filepath: str, content: str, formatting: dict)
    
    @staticmethod
    def get_file_extension(filepath: str) -> str
    
    @staticmethod
    def is_valid_path(filepath: str) -> bool
```

**Паттерны**:
- **Static Methods**: Утилитные функции без состояния
- **Adapter**: Адаптация различных форматов файлов

### 5. ui_components.py
**Назначение**: Переиспользуемые UI компоненты (View)

**Ответственность**:
- AI панель с чатом
- Панель форматирования
- Строка состояния
- Диалоги

**Компоненты**:

#### AIPanel
```python
class AIPanel(ctk.CTkFrame):
    def __init__(self, parent, ai_callback: Callable)
    def send_message(self)
    def quick_action(self, action: str)
    def add_message(self, message: str, sender: str)
    def clear_history(self)
    def toggle_visibility(self)
```

#### FormattingToolbar
```python
class FormattingToolbar(ctk.CTkFrame):
    def __init__(self, parent, callbacks: dict)
    # Содержит кнопки форматирования
```

#### StatusBar
```python
class StatusBar(ctk.CTkFrame):
    def __init__(self, parent)
    def update_counts(self, text: str)
    def set_save_status(self, status: str)
    def set_ai_status(self, status: str)
```

#### TemplateDialog
```python
class TemplateDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback: Callable)
    def generate(self)
```

**Паттерны**:
- **Composite**: Композиция UI элементов
- **Template Method**: Базовая структура диалогов

## Поток данных

### 1. Запуск приложения

```
main.py
  └─> TextEditor.__init__()
        ├─> load_config()
        ├─> setup_ai()
        │     └─> AIAssistant.__init__()
        ├─> setup_ui()
        │     ├─> setup_menu()
        │     ├─> setup_toolbar()
        │     ├─> setup_editor()
        │     ├─> setup_ai_panel()
        │     │     └─> AIPanel.__init__()
        │     └─> setup_statusbar()
        │           └─> StatusBar.__init__()
        └─> setup_bindings()
```

### 2. AI запрос (улучшение текста)

```
User выделяет текст и нажимает "Улучшить"
  ↓
AIPanel.quick_action("improve")
  ↓
TextEditor.handle_ai_action("improve", None)
  ↓
TextEditor.ai_action("improve")
  ↓
AIAssistant.improve_text(text, callback)
  ↓
AIAssistant.generate_async(prompt, callback)
  ↓
[Отдельный поток]
  ├─> Отправка запроса в Gemini API
  ├─> Получение ответа
  └─> callback(response, None)
        ↓
TextEditor.handle_ai_text_response(response, error)
  ↓
Замена текста в редакторе
  ↓
Обновление AI панели
  ↓
Обновление статус-бара
```

### 3. Сохранение файла

```
User нажимает Ctrl+S или "Сохранить"
  ↓
TextEditor.save_file()
  ↓
TextEditor.save_to_file(filepath)
  ↓
Получение содержимого из text_editor
  ↓
Определение расширения файла
  ↓
FileOperations.save_txt() или FileOperations.save_docx()
  ↓
Запись на диск
  ↓
Обновление статус-бара: "✓ Сохранено"
```

## Обработка ошибок

### Уровни обработки

1. **UI уровень** (editor.py)
   - `try-except` блоки для пользовательских действий
   - `messagebox` для отображения ошибок

2. **API уровень** (ai_assistant.py)
   - Обработка сетевых ошибок
   - Обработка ошибок API (401, 429, 500)
   - Передача ошибок через callback

3. **Файловый уровень** (file_operations.py)
   - `FileNotFoundError`, `PermissionError`
   - Логирование ошибок
   - Пробрасывание исключений вверх

### Пример обработки

```python
# editor.py
def save_file(self):
    try:
        content = self.text_editor.get("1.0", "end-1c")
        FileOperations.save_txt(self.current_file, content)
        self.statusbar.set_save_status("✓ Сохранено")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        messagebox.showerror("Ошибка", "Файл не найден")
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        messagebox.showerror("Ошибка", "Нет прав на запись")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")
```

## Конфигурация

### Структура config.ini

```ini
[API]
gemini_api_key = ...

[AI_SETTINGS]
model = gemini-pro
temperature = 0.7
max_tokens = 2048

[EDITOR]
autosave_interval = 60
default_font = Arial
default_font_size = 12
theme = light
```

### Загрузка конфигурации

```python
def load_config(self):
    self.config = configparser.ConfigParser()
    self.config.read('config.ini')
    
    api_key = self.config.get('API', 'gemini_api_key')
    model = self.config.get('AI_SETTINGS', 'model')
    temperature = float(self.config.get('AI_SETTINGS', 'temperature'))
```

## Логирование

### Конфигурация

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Использование

```python
logger.debug("Детальная информация")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка", exc_info=True)
logger.critical("Критическая ошибка")
```

## Тестирование

### Уровни тестирования

1. **Unit тесты** (test_basic.py)
   - Тестирование отдельных функций
   - Проверка импортов
   - Валидация конфигурации

2. **Integration тесты** (планируются)
   - Тестирование взаимодействия компонентов
   - Тестирование файловых операций
   - Mock API для тестирования AI функций

3. **UI тесты** (планируются)
   - Автоматизированное тестирование интерфейса
   - Сценарии пользовательских действий

## Производительность

### Оптимизации

1. **Асинхронные AI запросы**
   - Не блокируют UI
   - Используют отдельные потоки

2. **Ленивая загрузка**
   - AI модель инициализируется только при первом использовании
   - Компоненты UI создаются по требованию

3. **Автосохранение**
   - Работает в фоне
   - Не мешает редактированию

### Ограничения

- Большие документы (>100,000 слов) могут быть медленными
- AI запросы зависят от скорости интернета
- PDF экспорт может быть медленным для длинных документов

## Безопасность

### Обработка API ключа

1. **Хранение**: В config.ini (не в Git)
2. **Валидация**: Проверка перед использованием
3. **Логирование**: Ключ никогда не логируется

### Обработка пользовательских данных

1. **Локальное хранение**: Документы только на компьютере пользователя
2. **AI запросы**: Данные отправляются в Google, не рекомендуется для конфиденциальной информации
3. **Валидация**: Проверка путей файлов для предотвращения path traversal

## Расширяемость

### Добавление нового AI действия

1. Добавить метод в `AIAssistant`:
```python
def my_new_action(self, text: str, callback: Callable):
    prompt = f"Ваш промпт: {text}"
    self.generate_async(prompt, callback)
```

2. Добавить обработчик в `TextEditor`:
```python
def ai_action(self, action: str):
    # ...
    if action == "my_new_action":
        self.ai_assistant.my_new_action(text, self.handle_ai_text_response)
```

3. Добавить кнопку в UI:
```python
# в ui_components.py или editor.py
btn = ctk.CTkButton(text="Новое действие", command=lambda: self.ai_action("my_new_action"))
```

### Добавление нового формата файла

1. Добавить методы в `FileOperations`:
```python
@staticmethod
def open_markdown(filepath: str) -> str:
    # Код открытия .md файла
    pass

@staticmethod
def save_markdown(filepath: str, content: str):
    # Код сохранения .md файла
    pass
```

2. Обновить обработку в `TextEditor`:
```python
def open_file(self):
    # ...
    elif ext == '.md':
        content = FileOperations.open_markdown(filepath)
```

## Roadmap

### Версия 1.1.0
- Поддержка Markdown
- Вставка изображений
- Проверка орфографии (language-tool)

### Версия 1.2.0
- Расширенные таблицы
- Экспорт в HTML
- История версий документа

### Версия 2.0.0
- Система плагинов
- Поддержка других AI моделей (GPT-4, Claude)
- Совместное редактирование
- Облачная синхронизация

## Заключение

AI Text Editor построен на принципах:
- **Модульность**: Четкое разделение компонентов
- **Расширяемость**: Легко добавлять новые функции
- **Асинхронность**: Не блокирующий UI
- **Надежность**: Обработка ошибок на всех уровнях
- **Простота**: Понятная структура кода

---

**Автор**: AI Text Editor Team  
**Последнее обновление**: 31 октября 2024
