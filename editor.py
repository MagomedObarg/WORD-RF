import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
import tkinter.font as tkfont
from ai_assistant import AIAssistant
from file_operations import FileOperations
from ui_components import (AIPanel, FormattingToolbar, StatusBar, TemplateDialog,
                           StyleDialog, SettingsDialog, KeyboardShortcutsDialog,
                           WelcomeDialog, ProgressDialog)
import configparser
import os
import logging
import time
import threading
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TextEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Text Editor - Gemini")
        self.geometry("1400x800")
        
        self.current_file = None
        self.is_modified = False
        self.undo_stack = []
        self.redo_stack = []
        self.autosave_timer = None
        self.recent_files = []
        self.zoom_level = 1.0
        self.base_font_size = 12
        self.progress_dialog = None
        self.is_fullscreen = False
        
        self.load_config()
        self.load_recent_files()
        self.setup_ai()
        self.setup_ui()
        self.setup_bindings()
        self.start_autosave()
        
        self.after(500, self.show_welcome_if_needed)
        
        logger.info("Text Editor initialized")
    
    def load_config(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        
        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            self.config['API'] = {'gemini_api_key': 'YOUR_GEMINI_API_KEY_HERE'}
            self.config['AI_SETTINGS'] = {
                'model': 'gemini-pro',
                'temperature': '0.7',
                'max_tokens': '2048'
            }
            self.config['EDITOR'] = {
                'autosave_interval': '60',
                'default_font': 'Arial',
                'default_font_size': '12',
                'theme': 'light'
            }
            with open(config_path, 'w') as f:
                self.config.write(f)
    
    def setup_ai(self):
        api_key = self.config.get('API', 'gemini_api_key', fallback='')
        model = self.config.get('AI_SETTINGS', 'model', fallback='gemini-pro')
        temperature = float(self.config.get('AI_SETTINGS', 'temperature', fallback='0.7'))
        
        self.ai_assistant = AIAssistant(api_key, model, temperature)
        
        if not self.ai_assistant.is_ready():
            logger.warning("AI Assistant not configured properly")
    
    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.setup_menu()
        self.setup_toolbar()
        self.setup_editor()
        self.setup_ai_panel()
        self.setup_statusbar()
    
    def setup_menu(self):
        menubar = ctk.CTkFrame(self, height=40)
        menubar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        menu_buttons = [
            ("📁 Файл", self.show_file_menu),
            ("✏️ Правка", self.show_edit_menu),
            ("🎨 Формат", self.show_format_menu),
            ("🤖 AI", self.show_ai_menu),
            ("🔍 Вид", self.show_view_menu),
            ("⚙️ Настройки", self.show_settings),
            ("❓ Справка", self.show_help_menu)
        ]
        
        for text, command in menu_buttons:
            btn = ctk.CTkButton(
                menubar,
                text=text,
                command=command,
                width=100,
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            btn.pack(side="left", padx=5)
        
        theme_btn = ctk.CTkButton(
            menubar,
            text="🌙",
            command=self.toggle_theme,
            width=40,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        theme_btn.pack(side="right", padx=5)
        self.theme_btn = theme_btn
    
    def setup_toolbar(self):
        formatting_callbacks = {
            'font_change': self.change_font,
            'size_change': self.change_size,
            'bold': self.toggle_bold,
            'italic': self.toggle_italic,
            'underline': self.toggle_underline,
            'strikethrough': self.toggle_strikethrough,
            'align': self.change_alignment,
            'color': self.change_color
        }
        
        self.toolbar = FormattingToolbar(self, formatting_callbacks)
        self.toolbar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
    
    def setup_editor(self):
        editor_frame = ctk.CTkFrame(self)
        editor_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        self.text_editor = ctk.CTkTextbox(
            editor_frame,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        self.text_editor.grid(row=0, column=0, sticky="nsew")
        self.text_editor.bind('<KeyRelease>', self.on_text_change)
        self.text_editor.bind('<Button-3>', self.show_context_menu)
    
    def setup_ai_panel(self):
        self.ai_panel = AIPanel(self, self.handle_ai_action)
        self.ai_panel.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
        
        toggle_btn = ctk.CTkButton(
            self,
            text="◀",
            width=30,
            command=self.toggle_ai_panel
        )
        toggle_btn.grid(row=2, column=3, sticky="ns", pady=5)
        self.ai_toggle_btn = toggle_btn
    
    def setup_statusbar(self):
        self.statusbar = StatusBar(self)
        self.statusbar.grid(row=3, column=0, columnspan=4, sticky="ew")
    
    def setup_bindings(self):
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-S>', lambda e: self.save_file_as())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-z>', lambda e: self.undo())
        self.bind('<Control-y>', lambda e: self.redo())
        self.bind('<Control-f>', lambda e: self.find_replace())
        self.bind('<Control-Shift-A>', lambda e: self.show_ai_menu())
        self.bind('<Control-i>', lambda e: self.ai_action("improve"))
        self.bind('<Control-r>', lambda e: self.show_rewrite_dialog())
        self.bind('<Control-plus>', lambda e: self.zoom_in())
        self.bind('<Control-equal>', lambda e: self.zoom_in())
        self.bind('<Control-minus>', lambda e: self.zoom_out())
        self.bind('<Control-0>', lambda e: self.reset_zoom())
        self.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.bind('<F1>', lambda e: KeyboardShortcutsDialog(self))
    
    def show_file_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Файл")
        menu.geometry("250x350")
        menu.transient(self)
        
        options = [
            ("📄 Новый", self.new_file),
            ("📁 Открыть", self.open_file),
            ("💾 Сохранить", self.save_file),
            ("💾 Сохранить как", self.save_file_as),
            ("📤 Экспорт в PDF", self.export_pdf),
            ("📤 Экспорт в Markdown", self.export_markdown),
            ("📤 Экспорт в HTML", self.export_html),
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
        
        if self.recent_files:
            ctk.CTkLabel(menu, text="Недавние файлы:", font=ctk.CTkFont(weight="bold")).pack(padx=10, pady=(10, 5))
            for i, file in enumerate(self.recent_files[:3]):
                btn = ctk.CTkButton(
                    menu,
                    text=f"{i+1}. {os.path.basename(file)}",
                    command=lambda f=file, m=menu: (self.open_recent_file(f), m.destroy()),
                    fg_color="transparent",
                    border_width=1
                )
                btn.pack(padx=10, pady=2, fill="x")
        
        ctk.CTkButton(menu, text="❌ Выход", command=self.quit, fg_color="red").pack(padx=10, pady=10, fill="x")
    
    def show_edit_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Правка")
        menu.geometry("200x200")
        menu.transient(self)
        
        options = [
            ("↶ Отменить", self.undo),
            ("↷ Повторить", self.redo),
            ("🔍 Найти и заменить", self.find_replace),
            ("📊 Статистика", self.show_statistics)
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
    
    def show_format_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Формат")
        menu.geometry("200x150")
        menu.transient(self)
        
        options = [
            ("🎨 Цвет текста", self.change_color),
            ("📏 Отступы", self.adjust_spacing),
            ("🔤 Регистр", self.change_case)
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
    
    def show_ai_menu(self):
        if not self.ai_assistant.is_ready():
            messagebox.showwarning(
                "AI не настроен",
                "Пожалуйста, добавьте ваш Gemini API ключ в файл config.ini"
            )
            return
        
        menu = ctk.CTkToplevel(self)
        menu.title("AI Ассистент")
        menu.geometry("250x300")
        menu.transient(self)
        
        options = [
            ("✨ Улучшить текст", lambda: self.ai_action("improve")),
            ("🔄 Переписать", lambda: self.ai_action("rewrite")),
            ("➕ Продолжить текст", lambda: self.ai_action("continue")),
            ("✅ Исправить грамматику", lambda: self.ai_action("grammar")),
            ("📝 Сократить", lambda: self.ai_action("shorten")),
            ("📈 Расширить", lambda: self.ai_action("expand")),
            ("🌐 Перевести", lambda: self.ai_action("translate")),
            ("📋 Резюмировать", lambda: self.ai_action("summarize")),
            ("📄 Создать документ", lambda: self.show_template_dialog())
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
    
    def show_view_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Вид")
        menu.geometry("250x250")
        menu.transient(self)
        
        options = [
            ("➕ Увеличить (Ctrl++)", self.zoom_in),
            ("➖ Уменьшить (Ctrl+-)", self.zoom_out),
            ("🔄 Сбросить масштаб (Ctrl+0)", self.reset_zoom),
            ("⬛ Полный экран (F11)", self.toggle_fullscreen),
            ("📋 Панель AI", self.toggle_ai_panel),
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
    
    def show_help_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Справка")
        menu.geometry("250x200")
        menu.transient(self)
        
        options = [
            ("⌨️ Горячие клавиши (F1)", lambda: KeyboardShortcutsDialog(self)),
            ("👋 Приветствие", lambda: WelcomeDialog(self, self.show_settings)),
            ("ℹ️ О программе", self.show_about),
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                menu,
                text=text,
                command=lambda c=command, m=menu: (c(), m.destroy())
            )
            btn.pack(padx=10, pady=5, fill="x")
    
    def show_about(self):
        about_text = """
🤖 AI Text Editor - Gemini
Версия 1.0.0

Современный текстовый редактор с AI-ассистентом
на базе Google Gemini.

Возможности:
• Умное редактирование текста
• AI-генерация и улучшение
• Поддержка множества форматов
• Богатое форматирование

Разработано с ❤️ и AI

© 2024 AI Text Editor Team
        """
        messagebox.showinfo("О программе", about_text)
    
    def show_context_menu(self, event):
        if not self.ai_assistant.is_ready():
            return
        
        try:
            if self.text_editor.tag_ranges("sel"):
                menu = ctk.CTkToplevel(self)
                menu.overrideredirect(True)
                menu.geometry(f"+{event.x_root}+{event.y_root}")
                
                options = [
                    ("✨ Улучшить с AI", lambda: self.ai_action("improve")),
                    ("🔄 Переписать", lambda: self.ai_action("rewrite")),
                    ("➕ Продолжить", lambda: self.ai_action("continue"))
                ]
                
                for text, command in options:
                    btn = ctk.CTkButton(
                        menu,
                        text=text,
                        command=lambda c=command, m=menu: (c(), m.destroy()),
                        width=150
                    )
                    btn.pack(padx=5, pady=2)
                
                menu.after(3000, menu.destroy)
        except:
            pass
    
    def new_file(self):
        if self.is_modified:
            if messagebox.askyesno("Сохранить?", "Сохранить изменения перед созданием нового файла?"):
                self.save_file()
        
        self.text_editor.delete("1.0", "end")
        self.current_file = None
        self.is_modified = False
        self.title("AI Text Editor - Gemini")
    
    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx"),
                ("All Files", "*.*")
            ]
        )
        
        if filepath:
            try:
                ext = FileOperations.get_file_extension(filepath)
                
                if ext == '.txt':
                    content = FileOperations.open_txt(filepath)
                elif ext == '.docx':
                    content = FileOperations.open_docx(filepath)
                else:
                    content = FileOperations.open_txt(filepath)
                
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)
                self.current_file = filepath
                self.is_modified = False
                self.title(f"AI Text Editor - {os.path.basename(filepath)}")
                self.statusbar.set_save_status("✓ Файл загружен")
                self.add_recent_file(filepath)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
    
    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx"),
                ("All Files", "*.*")
            ]
        )
        
        if filepath:
            self.save_to_file(filepath)
            self.current_file = filepath
            self.title(f"AI Text Editor - {os.path.basename(filepath)}")
    
    def save_to_file(self, filepath: str):
        try:
            content = self.text_editor.get("1.0", "end-1c")
            ext = FileOperations.get_file_extension(filepath)
            
            if ext == '.docx':
                FileOperations.save_docx(filepath, content)
            else:
                FileOperations.save_txt(filepath, content)
            
            self.is_modified = False
            self.statusbar.set_save_status("✓ Сохранено")
            self.after(2000, lambda: self.statusbar.set_save_status(""))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def export_pdf(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if filepath:
            try:
                content = self.text_editor.get("1.0", "end-1c")
                FileOperations.export_pdf(filepath, content)
                messagebox.showinfo("Успех", "PDF экспортирован успешно")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать PDF: {e}")
    
    def on_text_change(self, event=None):
        self.is_modified = True
        content = self.text_editor.get("1.0", "end-1c")
        self.statusbar.update_counts(content)
    
    def undo(self):
        try:
            self.text_editor.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.text_editor.edit_redo()
        except:
            pass
    
    def find_replace(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Найти и заменить")
        dialog.geometry("400x200")
        dialog.transient(self)
        
        ctk.CTkLabel(dialog, text="Найти:").pack(padx=10, pady=(10, 0))
        find_entry = ctk.CTkEntry(dialog, width=350)
        find_entry.pack(padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="Заменить на:").pack(padx=10, pady=(10, 0))
        replace_entry = ctk.CTkEntry(dialog, width=350)
        replace_entry.pack(padx=10, pady=5)
        
        def do_replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_editor.get("1.0", "end-1c")
            new_content = content.replace(find_text, replace_text)
            self.text_editor.delete("1.0", "end")
            self.text_editor.insert("1.0", new_content)
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="Заменить все", command=do_replace).pack(pady=10)
    
    def show_statistics(self):
        content = self.text_editor.get("1.0", "end-1c")
        words = len(content.split())
        chars = len(content)
        chars_no_spaces = len(content.replace(" ", "").replace("\n", ""))
        lines = content.count("\n") + 1
        reading_time = max(1, words // 200)
        
        stats = f"""
Статистика документа:

Слов: {words}
Символов: {chars}
Символов без пробелов: {chars_no_spaces}
Строк: {lines}
Время чтения: ~{reading_time} мин
        """
        
        messagebox.showinfo("Статистика", stats)
    
    def change_font(self, font_name: str):
        try:
            if self.text_editor.tag_ranges("sel"):
                current_font = self.text_editor.cget("font")
                size = 12
                self.text_editor.configure(font=(font_name, size))
        except:
            pass
    
    def change_size(self, size: str):
        try:
            font_size = int(size)
            current_font = self.text_editor.cget("font")
            if isinstance(current_font, str):
                font_name = "Arial"
            else:
                font_name = current_font.split()[0] if current_font else "Arial"
            self.text_editor.configure(font=(font_name, font_size))
        except:
            pass
    
    def toggle_bold(self):
        pass
    
    def toggle_italic(self):
        pass
    
    def toggle_underline(self):
        pass
    
    def toggle_strikethrough(self):
        pass
    
    def change_alignment(self, align: str):
        pass
    
    def change_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста")
        if color[1]:
            try:
                self.text_editor.configure(fg_color=color[1])
            except:
                pass
    
    def adjust_spacing(self):
        pass
    
    def change_case(self):
        try:
            if self.text_editor.tag_ranges("sel"):
                selected = self.text_editor.get("sel.first", "sel.last")
                self.text_editor.delete("sel.first", "sel.last")
                self.text_editor.insert("insert", selected.upper())
        except:
            pass
    
    def toggle_ai_panel(self):
        if self.ai_panel.is_visible:
            self.ai_panel.grid_remove()
            self.ai_toggle_btn.configure(text="▶")
        else:
            self.ai_panel.grid()
            self.ai_toggle_btn.configure(text="◀")
        self.ai_panel.is_visible = not self.ai_panel.is_visible
    
    def handle_ai_action(self, action: str, data):
        if not self.ai_assistant.is_ready():
            self.ai_panel.add_message("AI не настроен. Добавьте API ключ в config.ini", "system")
            return
        
        if action == "chat":
            self.statusbar.set_ai_status("🤖 AI обрабатывает...")
            self.ai_assistant.chat(data, self.handle_ai_response)
        else:
            self.ai_action(action)
    
    def ai_action(self, action: str):
        if not self.ai_assistant.is_ready():
            messagebox.showwarning(
                "AI не настроен",
                "Пожалуйста, добавьте ваш Gemini API ключ в файл config.ini"
            )
            return
        
        try:
            selected_text = self.text_editor.get("sel.first", "sel.last")
        except:
            if action in ["improve", "rewrite", "grammar", "shorten", "expand"]:
                messagebox.showinfo("Выделите текст", "Пожалуйста, выделите текст для обработки")
                return
            selected_text = self.text_editor.get("1.0", "end-1c")
        
        if not selected_text.strip():
            messagebox.showinfo("Пустой текст", "Нет текста для обработки")
            return
        
        self.show_progress("🤖 AI обрабатывает ваш текст...")
        self.statusbar.set_ai_status("🤖 AI обрабатывает...")
        
        action_map = {
            "improve": self.ai_assistant.improve_text,
            "rewrite": lambda text, cb: self.ai_assistant.rewrite_text(text, "formal", cb),
            "continue": self.ai_assistant.continue_text,
            "grammar": self.ai_assistant.fix_grammar,
            "shorten": self.ai_assistant.shorten_text,
            "expand": self.ai_assistant.expand_text,
            "translate": lambda text, cb: self.show_translate_dialog(text, cb),
            "summarize": self.ai_assistant.summarize_text
        }
        
        if action in action_map:
            if action == "translate":
                action_map[action](selected_text, None)
            else:
                action_map[action](selected_text, self.handle_ai_text_response)
    
    def show_translate_dialog(self, text: str, callback):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Перевести")
        dialog.geometry("300x150")
        dialog.transient(self)
        
        ctk.CTkLabel(dialog, text="Целевой язык:").pack(padx=10, pady=10)
        
        lang_combo = ctk.CTkComboBox(
            dialog,
            values=["английский", "русский", "немецкий", "французский", "испанский", "китайский"]
        )
        lang_combo.set("английский")
        lang_combo.pack(padx=10, pady=5)
        
        def do_translate():
            target_lang = lang_combo.get()
            self.ai_assistant.translate_text(text, target_lang, self.handle_ai_text_response)
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="Перевести", command=do_translate).pack(pady=10)
    
    def show_template_dialog(self):
        TemplateDialog(self, self.handle_template_generation)
    
    def handle_template_generation(self, doc_type: str, description: str):
        self.statusbar.set_ai_status("🤖 AI создает документ...")
        self.ai_assistant.generate_document(doc_type, description, self.handle_ai_document_response)
    
    def handle_ai_response(self, response: str, error: Optional[str]):
        self.statusbar.set_ai_status("")
        
        if error:
            self.ai_panel.add_message(f"Ошибка: {error}", "system")
        else:
            self.ai_panel.add_message(response, "ai")
    
    def handle_ai_text_response(self, response: str, error: Optional[str]):
        self.hide_progress()
        self.statusbar.set_ai_status("")
        
        if error:
            messagebox.showerror("AI Ошибка", error)
            self.ai_panel.add_message(f"Ошибка: {error}", "system")
        else:
            try:
                start_idx = self.text_editor.index("sel.first")
                end_idx = self.text_editor.index("sel.last")
                self.text_editor.delete(start_idx, end_idx)
                self.text_editor.insert(start_idx, response)
            except:
                self.text_editor.insert("end", "\n\n" + response)
            
            self.ai_panel.add_message("Текст обработан успешно", "ai")
    
    def handle_ai_document_response(self, response: str, error: Optional[str]):
        self.hide_progress()
        self.statusbar.set_ai_status("")
        
        if error:
            messagebox.showerror("AI Ошибка", error)
        else:
            self.text_editor.delete("1.0", "end")
            self.text_editor.insert("1.0", response)
            self.ai_panel.add_message("Документ создан", "ai")
    
    def start_autosave(self):
        interval = int(self.config.get('EDITOR', 'autosave_interval', fallback='60'))
        
        def autosave():
            if self.is_modified and self.current_file:
                try:
                    self.save_to_file(self.current_file)
                    logger.info("Autosaved")
                except:
                    pass
            self.autosave_timer = self.after(interval * 1000, autosave)
        
        self.autosave_timer = self.after(interval * 1000, autosave)
    
    def load_recent_files(self):
        recent_file_path = os.path.join(os.path.dirname(__file__), 'recent_files.json')
        if os.path.exists(recent_file_path):
            try:
                with open(recent_file_path, 'r', encoding='utf-8') as f:
                    self.recent_files = json.load(f)
            except:
                self.recent_files = []
    
    def save_recent_files(self):
        recent_file_path = os.path.join(os.path.dirname(__file__), 'recent_files.json')
        try:
            with open(recent_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.recent_files[:10], f)
        except:
            pass
    
    def add_recent_file(self, filepath: str):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.save_recent_files()
    
    def open_recent_file(self, filepath: str):
        if os.path.exists(filepath):
            try:
                ext = FileOperations.get_file_extension(filepath)
                if ext == '.txt':
                    content = FileOperations.open_txt(filepath)
                elif ext == '.docx':
                    content = FileOperations.open_docx(filepath)
                else:
                    content = FileOperations.open_txt(filepath)
                
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)
                self.current_file = filepath
                self.is_modified = False
                self.title(f"AI Text Editor - {os.path.basename(filepath)}")
                self.statusbar.set_save_status("✓ Файл загружен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
        else:
            messagebox.showerror("Ошибка", "Файл не найден")
            self.recent_files.remove(filepath)
            self.save_recent_files()
    
    def export_markdown(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md")]
        )
        if filepath:
            try:
                content = self.text_editor.get("1.0", "end-1c")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Успех", "Markdown файл сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def export_html(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")]
        )
        if filepath:
            try:
                content = self.text_editor.get("1.0", "end-1c")
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }}
    </style>
</head>
<body>
    <pre>{content}</pre>
</body>
</html>"""
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Успех", "HTML файл сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def zoom_in(self):
        self.zoom_level = min(3.0, self.zoom_level + 0.1)
        self.apply_zoom()
    
    def zoom_out(self):
        self.zoom_level = max(0.5, self.zoom_level - 0.1)
        self.apply_zoom()
    
    def reset_zoom(self):
        self.zoom_level = 1.0
        self.apply_zoom()
    
    def apply_zoom(self):
        new_size = int(self.base_font_size * self.zoom_level)
        self.text_editor.configure(font=ctk.CTkFont(size=new_size))
        self.statusbar.set_save_status(f"Масштаб: {int(self.zoom_level * 100)}%")
        self.after(1000, lambda: self.statusbar.set_save_status(""))
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
    
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "Light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_btn.configure(text="☀️" if new_mode == "dark" else "🌙")
        self.config.set('EDITOR', 'theme', new_mode)
        self.save_config()
    
    def show_settings(self):
        SettingsDialog(self, self.config, self.apply_settings)
    
    def apply_settings(self):
        self.save_config()
        theme = self.config.get('EDITOR', 'theme', fallback='light')
        ctk.set_appearance_mode(theme)
        self.base_font_size = int(self.config.get('EDITOR', 'default_font_size', fallback='12'))
        self.apply_zoom()
        self.setup_ai()
        messagebox.showinfo("Настройки", "Настройки сохранены и применены")
    
    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)
    
    def show_rewrite_dialog(self):
        try:
            selected_text = self.text_editor.get("sel.first", "sel.last")
            if not selected_text.strip():
                messagebox.showinfo("Выделите текст", "Пожалуйста, выделите текст для переписывания")
                return
            
            def apply_rewrite(style):
                self.show_progress("🤖 AI переписывает текст...")
                self.ai_assistant.rewrite_text(selected_text, style, self.handle_ai_text_response)
            
            StyleDialog(self, apply_rewrite)
        except:
            messagebox.showinfo("Выделите текст", "Пожалуйста, выделите текст для переписывания")
    
    def show_progress(self, message: str):
        if self.progress_dialog:
            self.progress_dialog.close()
        self.progress_dialog = ProgressDialog(self, message)
    
    def hide_progress(self):
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
    
    def show_welcome_if_needed(self):
        welcome_file = os.path.join(os.path.dirname(__file__), '.welcome_shown')
        if not os.path.exists(welcome_file):
            WelcomeDialog(self, self.show_settings)
            try:
                with open(welcome_file, 'w') as f:
                    f.write('1')
            except:
                pass
    
    def quit(self):
        if self.is_modified:
            if messagebox.askyesno("Сохранить?", "Сохранить изменения перед выходом?"):
                self.save_file()
        
        if self.autosave_timer:
            self.after_cancel(self.autosave_timer)
        
        self.destroy()


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
