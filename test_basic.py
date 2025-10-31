#!/usr/bin/env python3
"""
Базовые тесты для проверки работоспособности модулей
"""

import sys
import os

def test_imports():
    """Проверка импорта всех модулей"""
    print("Тестирование импортов...")
    
    try:
        import ai_assistant
        print("✓ ai_assistant импортирован")
    except Exception as e:
        print(f"✗ Ошибка импорта ai_assistant: {e}")
        return False
    
    try:
        import file_operations
        print("✓ file_operations импортирован")
    except Exception as e:
        print(f"✗ Ошибка импорта file_operations: {e}")
        return False
    
    try:
        import ui_components
        print("✓ ui_components импортирован")
    except Exception as e:
        print(f"✗ Ошибка импорта ui_components: {e}")
        return False
    
    try:
        import editor
        print("✓ editor импортирован")
    except Exception as e:
        print(f"✗ Ошибка импорта editor: {e}")
        return False
    
    return True


def test_config():
    """Проверка конфигурационного файла"""
    print("\nТестирование конфигурации...")
    
    if not os.path.exists('config.ini'):
        print("✗ config.ini не найден")
        return False
    
    print("✓ config.ini найден")
    
    import configparser
    config = configparser.ConfigParser()
    
    try:
        config.read('config.ini')
        
        if 'API' in config:
            print("✓ Секция [API] найдена")
        else:
            print("✗ Секция [API] не найдена")
            return False
        
        if 'AI_SETTINGS' in config:
            print("✓ Секция [AI_SETTINGS] найдена")
        else:
            print("✗ Секция [AI_SETTINGS] не найдена")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Ошибка чтения config.ini: {e}")
        return False


def test_ai_assistant():
    """Проверка AI ассистента"""
    print("\nТестирование AI ассистента...")
    
    try:
        from ai_assistant import AIAssistant
        
        # Тест с пустым ключом
        assistant = AIAssistant("test_key")
        print("✓ AIAssistant создан")
        
        # Проверка методов
        methods = [
            'is_ready', 'generate_async', 'improve_text', 
            'rewrite_text', 'continue_text', 'fix_grammar',
            'shorten_text', 'expand_text', 'translate_text',
            'summarize_text', 'generate_document', 'chat'
        ]
        
        for method in methods:
            if hasattr(assistant, method):
                print(f"✓ Метод {method} существует")
            else:
                print(f"✗ Метод {method} не найден")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Ошибка в AIAssistant: {e}")
        return False


def test_file_operations():
    """Проверка файловых операций"""
    print("\nТестирование файловых операций...")
    
    try:
        from file_operations import FileOperations
        
        # Проверка методов
        methods = [
            'new_document', 'open_txt', 'open_docx',
            'save_txt', 'save_docx', 'export_pdf',
            'get_file_extension', 'is_valid_path'
        ]
        
        for method in methods:
            if hasattr(FileOperations, method):
                print(f"✓ Метод {method} существует")
            else:
                print(f"✗ Метод {method} не найден")
                return False
        
        # Тест создания нового документа
        content = FileOperations.new_document()
        print("✓ new_document работает")
        
        # Тест получения расширения файла
        ext = FileOperations.get_file_extension("test.txt")
        if ext == ".txt":
            print("✓ get_file_extension работает")
        else:
            print("✗ get_file_extension возвращает неверное значение")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Ошибка в FileOperations: {e}")
        return False


def test_dependencies():
    """Проверка зависимостей"""
    print("\nПроверка зависимостей...")
    
    dependencies = {
        'customtkinter': 'CustomTkinter UI framework',
        'docx': 'python-docx для работы с .docx',
        'reportlab': 'ReportLab для PDF',
        'google.generativeai': 'Google Generative AI'
    }
    
    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} не установлен")
            all_ok = False
    
    return all_ok


def main():
    """Запуск всех тестов"""
    print("=" * 50)
    print("ЗАПУСК БАЗОВЫХ ТЕСТОВ")
    print("=" * 50)
    
    results = []
    
    # Запускаем тесты
    results.append(("Импорты", test_imports()))
    results.append(("Конфигурация", test_config()))
    results.append(("Зависимости", test_dependencies()))
    results.append(("AI Ассистент", test_ai_assistant()))
    results.append(("Файловые операции", test_file_operations()))
    
    # Результаты
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Пройдено: {passed}/{len(results)}")
    print(f"Провалено: {failed}/{len(results)}")
    print("=" * 50)
    
    if failed == 0:
        print("\n🎉 Все тесты пройдены успешно!")
        return 0
    else:
        print(f"\n⚠️ Провалено тестов: {failed}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
