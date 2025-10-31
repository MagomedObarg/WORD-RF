import customtkinter as ctk
from tkinter import colorchooser
from typing import Callable, Optional


class AIPanel(ctk.CTkFrame):
    def __init__(self, parent, ai_callback: Callable):
        super().__init__(parent, width=300)
        self.ai_callback = ai_callback
        self.is_visible = True
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkLabel(
            self, 
            text="🤖 AI Ассистент",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.chat_display = ctk.CTkTextbox(self, wrap="word")
        self.chat_display.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.chat_display.configure(state="disabled")
        
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_input = ctk.CTkEntry(input_frame, placeholder_text="Спросите AI...")
        self.chat_input.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="➤",
            width=40,
            command=self.send_message
        )
        send_btn.grid(row=0, column=1, pady=5)
        
        actions_label = ctk.CTkLabel(
            self,
            text="Быстрые действия:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        actions_label.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
        
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        actions = [
            ("✨ Улучшить", "improve"),
            ("🔄 Переписать", "rewrite"),
            ("➕ Продолжить", "continue"),
            ("✅ Грамматика", "grammar"),
            ("📝 Сократить", "shorten"),
            ("📈 Расширить", "expand"),
            ("🌐 Перевести", "translate"),
            ("📋 Резюме", "summarize")
        ]
        
        for idx, (label, action) in enumerate(actions):
            btn = ctk.CTkButton(
                actions_frame,
                text=label,
                command=lambda a=action: self.quick_action(a),
                height=28,
                font=ctk.CTkFont(size=11)
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
        
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        clear_btn = ctk.CTkButton(
            self,
            text="🗑️ Очистить историю",
            command=self.clear_history,
            fg_color="transparent",
            border_width=1
        )
        clear_btn.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")
    
    def send_message(self):
        message = self.chat_input.get().strip()
        if message:
            self.add_message(f"Вы: {message}", "user")
            self.chat_input.delete(0, 'end')
            self.ai_callback("chat", message)
    
    def quick_action(self, action: str):
        self.ai_callback(action, None)
    
    def add_message(self, message: str, sender: str = "ai"):
        self.chat_display.configure(state="normal")
        
        if sender == "user":
            self.chat_display.insert("end", f"\n{message}\n", "user")
        elif sender == "ai":
            self.chat_display.insert("end", f"\n🤖 AI: {message}\n", "ai")
        elif sender == "system":
            self.chat_display.insert("end", f"\n⚠️ {message}\n", "system")
        
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def clear_history(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
    
    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.grid()
        else:
            self.grid_remove()


class FormattingToolbar(ctk.CTkFrame):
    def __init__(self, parent, callbacks: dict):
        super().__init__(parent)
        self.callbacks = callbacks
        
        fonts = ["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia", "Comic Sans MS"]
        self.font_combo = ctk.CTkComboBox(
            self,
            values=fonts,
            width=140,
            command=lambda choice: callbacks.get('font_change', lambda x: None)(choice)
        )
        self.font_combo.set("Arial")
        self.font_combo.grid(row=0, column=0, padx=5, pady=5)
        
        sizes = [str(i) for i in range(8, 73, 2)]
        self.size_combo = ctk.CTkComboBox(
            self,
            values=sizes,
            width=70,
            command=lambda choice: callbacks.get('size_change', lambda x: None)(choice)
        )
        self.size_combo.set("12")
        self.size_combo.grid(row=0, column=1, padx=5, pady=5)
        
        self.bold_btn = ctk.CTkButton(
            self,
            text="B",
            width=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: callbacks.get('bold', lambda: None)()
        )
        self.bold_btn.grid(row=0, column=2, padx=2, pady=5)
        
        self.italic_btn = ctk.CTkButton(
            self,
            text="I",
            width=40,
            font=ctk.CTkFont(size=14, slant="italic"),
            command=lambda: callbacks.get('italic', lambda: None)()
        )
        self.italic_btn.grid(row=0, column=3, padx=2, pady=5)
        
        self.underline_btn = ctk.CTkButton(
            self,
            text="U",
            width=40,
            font=ctk.CTkFont(size=14, underline=True),
            command=lambda: callbacks.get('underline', lambda: None)()
        )
        self.underline_btn.grid(row=0, column=4, padx=2, pady=5)
        
        self.strike_btn = ctk.CTkButton(
            self,
            text="S",
            width=40,
            font=ctk.CTkFont(size=14, overstrike=True),
            command=lambda: callbacks.get('strikethrough', lambda: None)()
        )
        self.strike_btn.grid(row=0, column=5, padx=2, pady=5)
        
        align_frame = ctk.CTkFrame(self)
        align_frame.grid(row=0, column=6, padx=10, pady=5)
        
        self.left_btn = ctk.CTkButton(
            align_frame,
            text="⬅",
            width=35,
            command=lambda: callbacks.get('align', lambda x: None)('left')
        )
        self.left_btn.grid(row=0, column=0, padx=2)
        
        self.center_btn = ctk.CTkButton(
            align_frame,
            text="↔",
            width=35,
            command=lambda: callbacks.get('align', lambda x: None)('center')
        )
        self.center_btn.grid(row=0, column=1, padx=2)
        
        self.right_btn = ctk.CTkButton(
            align_frame,
            text="➡",
            width=35,
            command=lambda: callbacks.get('align', lambda x: None)('right')
        )
        self.right_btn.grid(row=0, column=2, padx=2)
        
        self.color_btn = ctk.CTkButton(
            self,
            text="🎨 Цвет",
            width=80,
            command=lambda: callbacks.get('color', lambda: None)()
        )
        self.color_btn.grid(row=0, column=7, padx=5, pady=5)


class StatusBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=30)
        
        self.word_count_label = ctk.CTkLabel(self, text="Слов: 0")
        self.word_count_label.pack(side="left", padx=10)
        
        self.char_count_label = ctk.CTkLabel(self, text="Символов: 0")
        self.char_count_label.pack(side="left", padx=10)
        
        self.save_status_label = ctk.CTkLabel(self, text="")
        self.save_status_label.pack(side="left", padx=10)
        
        self.ai_status_label = ctk.CTkLabel(self, text="")
        self.ai_status_label.pack(side="right", padx=10)
    
    def update_counts(self, text: str):
        words = len(text.split())
        chars = len(text)
        self.word_count_label.configure(text=f"Слов: {words}")
        self.char_count_label.configure(text=f"Символов: {chars}")
    
    def set_save_status(self, status: str):
        self.save_status_label.configure(text=status)
    
    def set_ai_status(self, status: str):
        self.ai_status_label.configure(text=status)


class TemplateDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback: Callable):
        super().__init__(parent)
        self.callback = callback
        self.title("Создать документ с AI")
        self.geometry("500x400")
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            self,
            text="Выберите тип документа:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        doc_types = [
            ("📧 Деловое письмо", "letter"),
            ("📄 Резюме", "resume"),
            ("📋 Договор", "contract"),
            ("📊 Отчет", "report"),
            ("📰 Статья", "article")
        ]
        
        self.doc_type_var = ctk.StringVar(value="letter")
        
        for label_text, value in doc_types:
            radio = ctk.CTkRadioButton(
                self,
                text=label_text,
                variable=self.doc_type_var,
                value=value
            )
            radio.grid(row=doc_types.index((label_text, value)) + 1, column=0, padx=20, pady=5, sticky="w")
        
        desc_label = ctk.CTkLabel(
            self,
            text="Опишите содержание документа:",
            font=ctk.CTkFont(size=12)
        )
        desc_label.grid(row=len(doc_types) + 1, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.description_text = ctk.CTkTextbox(self, height=100)
        self.description_text.grid(row=len(doc_types) + 2, column=0, padx=20, pady=5, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=len(doc_types) + 3, column=0, padx=20, pady=20, sticky="ew")
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="transparent",
            border_width=1
        )
        cancel_btn.pack(side="left", padx=5)
        
        generate_btn = ctk.CTkButton(
            btn_frame,
            text="✨ Создать с AI",
            command=self.generate
        )
        generate_btn.pack(side="right", padx=5)
    
    def generate(self):
        doc_type = self.doc_type_var.get()
        description = self.description_text.get("1.0", "end-1c").strip()
        
        if description:
            self.callback(doc_type, description)
            self.destroy()


class StyleDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback: Callable):
        super().__init__(parent)
        self.callback = callback
        self.title("Выберите стиль")
        self.geometry("400x300")
        self.transient(parent)
        
        label = ctk.CTkLabel(
            self,
            text="Выберите стиль для переписывания текста:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(padx=20, pady=20)
        
        styles = [
            ("📝 Формальный деловой", "formal"),
            ("💬 Неформальный дружеский", "informal"),
            ("💼 Деловой профессиональный", "business"),
            ("🎨 Творческий креативный", "creative"),
            ("📚 Академический научный", "academic")
        ]
        
        self.style_var = ctk.StringVar(value="formal")
        
        for label_text, value in styles:
            radio = ctk.CTkRadioButton(
                self,
                text=label_text,
                variable=self.style_var,
                value=value
            )
            radio.pack(padx=20, pady=8, anchor="w")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="transparent",
            border_width=1
        )
        cancel_btn.pack(side="left", padx=5)
        
        apply_btn = ctk.CTkButton(
            btn_frame,
            text="Применить",
            command=self.apply_style
        )
        apply_btn.pack(side="right", padx=5)
    
    def apply_style(self):
        style = self.style_var.get()
        self.callback(style)
        self.destroy()


class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, config, save_callback: Callable):
        super().__init__(parent)
        self.config = config
        self.save_callback = save_callback
        self.title("Настройки")
        self.geometry("600x500")
        self.transient(parent)
        
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab1 = tabview.add("Редактор")
        tab2 = tabview.add("AI")
        tab3 = tabview.add("Интерфейс")
        
        # Editor settings
        ctk.CTkLabel(tab1, text="Настройки редактора", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        font_frame = ctk.CTkFrame(tab1)
        font_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(font_frame, text="Шрифт по умолчанию:").pack(side="left", padx=10)
        self.font_var = ctk.StringVar(value=config.get('EDITOR', 'default_font', fallback='Arial'))
        font_combo = ctk.CTkComboBox(
            font_frame,
            values=["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia"],
            variable=self.font_var
        )
        font_combo.pack(side="right", padx=10)
        
        size_frame = ctk.CTkFrame(tab1)
        size_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(size_frame, text="Размер шрифта:").pack(side="left", padx=10)
        self.size_var = ctk.StringVar(value=config.get('EDITOR', 'default_font_size', fallback='12'))
        size_combo = ctk.CTkComboBox(
            size_frame,
            values=[str(i) for i in range(8, 32, 2)],
            variable=self.size_var
        )
        size_combo.pack(side="right", padx=10)
        
        autosave_frame = ctk.CTkFrame(tab1)
        autosave_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(autosave_frame, text="Автосохранение (сек):").pack(side="left", padx=10)
        self.autosave_var = ctk.StringVar(value=config.get('EDITOR', 'autosave_interval', fallback='60'))
        autosave_entry = ctk.CTkEntry(autosave_frame, textvariable=self.autosave_var, width=100)
        autosave_entry.pack(side="right", padx=10)
        
        # AI settings
        ctk.CTkLabel(tab2, text="Настройки AI", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        api_frame = ctk.CTkFrame(tab2)
        api_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(api_frame, text="API ключ:").pack(side="left", padx=10)
        self.api_var = ctk.StringVar(value=config.get('API', 'gemini_api_key', fallback=''))
        api_entry = ctk.CTkEntry(api_frame, textvariable=self.api_var, width=300, show="*")
        api_entry.pack(side="right", padx=10)
        
        temp_frame = ctk.CTkFrame(tab2)
        temp_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(temp_frame, text="Температура (креативность):").pack(side="left", padx=10)
        self.temp_var = ctk.StringVar(value=config.get('AI_SETTINGS', 'temperature', fallback='0.7'))
        temp_slider = ctk.CTkSlider(temp_frame, from_=0.0, to=1.0, variable=self.temp_var, number_of_steps=10)
        temp_slider.pack(side="right", padx=10, fill="x", expand=True)
        temp_label = ctk.CTkLabel(temp_frame, textvariable=self.temp_var, width=40)
        temp_label.pack(side="right", padx=5)
        
        # Interface settings
        ctk.CTkLabel(tab3, text="Настройки интерфейса", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        theme_frame = ctk.CTkFrame(tab3)
        theme_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(theme_frame, text="Тема:").pack(side="left", padx=10)
        self.theme_var = ctk.StringVar(value=config.get('EDITOR', 'theme', fallback='light'))
        theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=["light", "dark", "system"],
            variable=self.theme_var
        )
        theme_combo.pack(side="right", padx=10)
        
        # Save/Cancel buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="transparent",
            border_width=1
        )
        cancel_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            command=self.save_settings
        )
        save_btn.pack(side="right", padx=5)
    
    def save_settings(self):
        self.config.set('EDITOR', 'default_font', self.font_var.get())
        self.config.set('EDITOR', 'default_font_size', self.size_var.get())
        self.config.set('EDITOR', 'autosave_interval', self.autosave_var.get())
        self.config.set('EDITOR', 'theme', self.theme_var.get())
        self.config.set('API', 'gemini_api_key', self.api_var.get())
        self.config.set('AI_SETTINGS', 'temperature', str(float(self.temp_var.get())))
        
        self.save_callback()
        self.destroy()


class KeyboardShortcutsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Горячие клавиши")
        self.geometry("500x600")
        self.transient(parent)
        
        ctk.CTkLabel(
            self,
            text="⌨️ Горячие клавиши",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)
        
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=10, pady=5)
        
        shortcuts = [
            ("Файлы", [
                ("Ctrl+N", "Создать новый документ"),
                ("Ctrl+O", "Открыть файл"),
                ("Ctrl+S", "Сохранить"),
                ("Ctrl+Shift+S", "Сохранить как"),
            ]),
            ("Редактирование", [
                ("Ctrl+Z", "Отменить"),
                ("Ctrl+Y", "Повторить"),
                ("Ctrl+F", "Найти и заменить"),
                ("Ctrl+A", "Выделить всё"),
            ]),
            ("AI", [
                ("Ctrl+Shift+A", "Меню AI"),
                ("Ctrl+I", "Улучшить текст"),
                ("Ctrl+R", "Переписать"),
            ]),
            ("Вид", [
                ("Ctrl++", "Увеличить масштаб"),
                ("Ctrl+-", "Уменьшить масштаб"),
                ("Ctrl+0", "Сбросить масштаб"),
                ("F11", "Полноэкранный режим"),
            ])
        ]
        
        for category, items in shortcuts:
            cat_label = ctk.CTkLabel(
                scrollable,
                text=category,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            cat_label.pack(anchor="w", padx=10, pady=(15, 5))
            
            for key, desc in items:
                item_frame = ctk.CTkFrame(scrollable)
                item_frame.pack(fill="x", padx=10, pady=2)
                
                ctk.CTkLabel(
                    item_frame,
                    text=key,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=120
                ).pack(side="left", padx=10)
                
                ctk.CTkLabel(
                    item_frame,
                    text=desc,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=10)
        
        close_btn = ctk.CTkButton(
            self,
            text="Закрыть",
            command=self.destroy
        )
        close_btn.pack(pady=10)


class WelcomeDialog(ctk.CTkToplevel):
    def __init__(self, parent, config_callback: Callable):
        super().__init__(parent)
        self.config_callback = config_callback
        self.title("Добро пожаловать!")
        self.geometry("600x450")
        self.transient(parent)
        
        ctk.CTkLabel(
            self,
            text="🤖 AI Text Editor - Gemini",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            self,
            text="Современный текстовый редактор с AI-ассистентом",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        features = [
            "✨ Улучшение и переписывание текста",
            "🌐 Перевод на разные языки",
            "📝 Автоматическое исправление грамматики",
            "📄 Генерация документов с нуля",
            "💬 Чат с AI-ассистентом",
            "🎨 Богатое форматирование текста"
        ]
        
        for feature in features:
            ctk.CTkLabel(
                info_frame,
                text=feature,
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(
            self,
            text="Для использования AI нужен Gemini API ключ",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        start_btn = ctk.CTkButton(
            btn_frame,
            text="Начать работу",
            command=self.destroy,
            width=150
        )
        start_btn.pack(side="left", padx=10)
        
        config_btn = ctk.CTkButton(
            btn_frame,
            text="⚙️ Настроить API",
            command=self.open_config,
            width=150
        )
        config_btn.pack(side="left", padx=10)
    
    def open_config(self):
        self.config_callback()
        self.destroy()


class ProgressDialog(ctk.CTkToplevel):
    def __init__(self, parent, message: str):
        super().__init__(parent)
        self.title("Обработка")
        self.geometry("400x150")
        self.transient(parent)
        self.resizable(False, False)
        
        ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
        
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(padx=40, pady=10, fill="x")
        self.progress.start()
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Пожалуйста, подождите...",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(pady=5)
    
    def close(self):
        self.progress.stop()
        self.destroy()
