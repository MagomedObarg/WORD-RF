import customtkinter as ctk
from tkinter import colorchooser
from typing import Callable, Optional


class AIPanel(ctk.CTkFrame):
    def __init__(self, parent, ai_callback: Callable):
        super().__init__(parent, width=300)
        self.ai_callback = ai_callback
        self.is_visible = True
        self.message_count = 0
        self.has_history = False
        self.placeholder_active = False
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkLabel(
            header_frame, 
            text="🤖 AI Ассистент",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, sticky="w")
        
        self.message_count_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60")
        )
        self.message_count_label.grid(row=0, column=1, sticky="e", padx=(5, 0))
        
        self.chat_display = ctk.CTkTextbox(
            self, 
            wrap="word",
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.chat_display.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.chat_display.configure(state="disabled")
        
        self.system_message_font = ctk.CTkFont(size=11, slant="italic")
        self.chat_display.tag_config("user", justify="right", foreground=("#1B4F72", "#AED6F1"), spacing1=4, spacing3=4)
        self.chat_display.tag_config("ai", justify="left", foreground=("#145A32", "#A9DFBF"), spacing1=4, spacing3=4)
        self.chat_display.tag_config("system", justify="center", foreground=("gray40", "gray70"), font=self.system_message_font, spacing1=6, spacing3=6)
        
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_input = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Спросите AI...",
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        self.chat_input.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        self.chat_input.bind("<KeyRelease>", lambda e: self.update_send_button_state())
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="➤",
            width=50,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=16),
            command=self.send_message,
            state="disabled"
        )
        send_btn.grid(row=0, column=1, pady=5)
        self.send_btn = send_btn
        
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
                height=32,
                corner_radius=6,
                font=ctk.CTkFont(size=11),
                hover_color=("#3498db", "#2980b9")
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
        
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        separator = ctk.CTkFrame(self, height=2, fg_color=("gray70", "gray30"))
        separator.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        
        self.clear_btn = ctk.CTkButton(
            self,
            text="🗑️ Очистить историю",
            command=self.confirm_clear_history,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226"),
            text_color="white",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.clear_btn.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.update_send_button_state()
        self.update_clear_button_state()
        self.update_message_count_label()
        self.show_empty_state()
    
    def send_message(self):
        message = self.chat_input.get().strip()
        if not message:
            return
        self.add_message(message, "user")
        self.chat_input.delete(0, 'end')
        self.update_send_button_state()
        if callable(self.ai_callback):
            self.ai_callback("chat", message)
    
    def quick_action(self, action: str):
        if callable(self.ai_callback):
            self.ai_callback(action, None)
    
    def add_message(self, message: str, sender: str = "ai"):
        message = message.strip()
        if not message:
            return
        self.chat_display.configure(state="normal")
        existing_content = self.chat_display.get("1.0", "end-1c").strip()
        if existing_content:
            self.chat_display.insert("end", "\n\n")
        tag = "system"
        formatted_message = message
        if sender == "user":
            formatted_message = f"🙋 Вы: {message}"
            tag = "user"
            self.message_count += 1
        elif sender == "ai":
            formatted_message = f"🤖 AI: {message}"
            tag = "ai"
            self.message_count += 1
        else:
            if not message.startswith(("ℹ", "⚠", "✅", "💡", "🗑")):
                formatted_message = f"ℹ️ {message}"
        self.chat_display.insert("end", formatted_message, tag)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
        self.has_history = self.message_count > 0
        self.update_message_count_label()
        self.update_clear_button_state()
        self.update_send_button_state()
    
    def confirm_clear_history(self):
        from tkinter import messagebox
        result = messagebox.askyesno(
            "Подтверждение",
            "Вы уверены, что хотите очистить историю чата?\nЭто действие нельзя отменить.",
            icon='warning'
        )
        if result:
            self.clear_history()
    
    def clear_history(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.message_count = 0
        self.has_history = False
        self.update_message_count_label()
        self.update_clear_button_state()
    
    def update_message_count_label(self):
        if self.message_count > 0:
            self.message_count_label.configure(text=f"({self.message_count} сообщений)")
        else:
            self.message_count_label.configure(text="")
    
    def update_clear_button_state(self):
        if self.has_history:
            self.clear_btn.configure(state="normal")
        else:
            self.clear_btn.configure(state="disabled")
    
    def update_send_button_state(self):
        message = self.chat_input.get().strip()
        if message:
            self.send_btn.configure(state="normal")
        else:
            self.send_btn.configure(state="disabled")
    
    def show_empty_state(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        empty_message = "👋 Привет! Я ваш AI-ассистент.\n\nЗадайте мне вопрос или используйте быстрые действия ниже."
        self.chat_display.insert("1.0", empty_message)
        self.chat_display.tag_add("system", "1.0", "end")
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
        self.geometry("640x520")
        self.transient(parent)
        self.resizable(False, False)
        
        self._init_variables()
        self._build_ui()
    
    def _init_variables(self):
        self.font_var = ctk.StringVar(value=self.config.get('EDITOR', 'default_font', fallback='Arial'))
        self.size_var = ctk.StringVar(value=self.config.get('EDITOR', 'default_font_size', fallback='12'))
        self.autosave_var = ctk.StringVar(value=self.config.get('EDITOR', 'autosave_interval', fallback='60'))
        
        self.api_var = ctk.StringVar(value=self.config.get('API', 'gemini_api_key', fallback=''))
        self.model_var = ctk.StringVar(value=self.config.get('AI_SETTINGS', 'model', fallback='gemini-pro'))
        
        try:
            temperature = float(self.config.get('AI_SETTINGS', 'temperature', fallback='0.7'))
        except (ValueError, TypeError):
            temperature = 0.7
        temperature = max(0.0, min(1.0, temperature))
        self.temperature_var = ctk.DoubleVar(value=temperature)
        self.temperature_display_var = ctk.StringVar(value=f"{temperature:.1f}")
        
        self.max_tokens_options = ["512", "1024", "2048", "4096", "8192"]
        current_tokens = self.config.get('AI_SETTINGS', 'max_tokens', fallback='2048')
        if current_tokens not in self.max_tokens_options:
            current_tokens = '2048'
        self.max_tokens_var = ctk.StringVar(value=current_tokens)
        
        theme_value = self.config.get('INTERFACE', 'theme', fallback='light')
        if theme_value not in ("light", "dark", "system"):
            theme_value = "light"
        self.theme_var = ctk.StringVar(value=theme_value)
        
        self.ui_scale_map = {
            "80%": "0.8",
            "90%": "0.9",
            "100%": "1.0",
            "110%": "1.1",
            "120%": "1.2"
        }
        stored_scale = self.config.get('INTERFACE', 'ui_scale', fallback='1.0')
        default_scale_label = next((label for label, value in self.ui_scale_map.items() if value == stored_scale), "100%")
        self.ui_scale_choice_var = ctk.StringVar(value=default_scale_label)
        
        self.show_ai_panel_var = ctk.BooleanVar(value=self.config.getboolean('INTERFACE', 'show_ai_panel', fallback=True))
        self.show_statusbar_var = ctk.BooleanVar(value=self.config.getboolean('INTERFACE', 'show_statusbar', fallback=True))
        
        self.show_api_var = ctk.BooleanVar(value=False)
    
    def _build_ui(self):
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=12, pady=12)
        
        editor_tab = tabview.add("Редактор")
        ai_tab = tabview.add("AI")
        interface_tab = tabview.add("Интерфейс")
        
        self._build_editor_tab(editor_tab)
        self._build_ai_tab(ai_tab)
        self._build_interface_tab(interface_tab)
        self._build_actions()
    
    def _build_editor_tab(self, tab):
        ctk.CTkLabel(tab, text="Настройки редактора", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 12))
        
        font_frame = ctk.CTkFrame(tab)
        font_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(font_frame, text="Шрифт по умолчанию:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            font_frame,
            values=["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia"],
            variable=self.font_var,
            width=180
        ).pack(side="right", padx=10)
        
        size_frame = ctk.CTkFrame(tab)
        size_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(size_frame, text="Размер шрифта:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            size_frame,
            values=[str(i) for i in range(8, 32, 2)],
            variable=self.size_var,
            width=100
        ).pack(side="right", padx=10)
        
        autosave_frame = ctk.CTkFrame(tab)
        autosave_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(autosave_frame, text="Автосохранение (сек):").pack(side="left", padx=10)
        ctk.CTkEntry(autosave_frame, textvariable=self.autosave_var, width=120).pack(side="right", padx=10)
    
    def _build_ai_tab(self, tab):
        ctk.CTkLabel(tab, text="Настройки AI", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 12))
        
        api_frame = ctk.CTkFrame(tab)
        api_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(api_frame, text="API ключ:").pack(side="left", padx=10)
        
        self.api_entry = ctk.CTkEntry(api_frame, textvariable=self.api_var, width=300, show="*")
        self.api_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        self.api_toggle_btn = ctk.CTkButton(
            api_frame,
            text="Показать",
            width=100,
            command=self.toggle_api_visibility
        )
        self.api_toggle_btn.pack(side="right", padx=10)
        
        model_frame = ctk.CTkFrame(tab)
        model_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(model_frame, text="Модель:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            model_frame,
            values=["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"],
            variable=self.model_var,
            width=200
        ).pack(side="right", padx=10)
        
        temp_frame = ctk.CTkFrame(tab)
        temp_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(temp_frame, text="Температура (креативность):").pack(side="left", padx=10)
        
        ctk.CTkLabel(
            temp_frame,
            textvariable=self.temperature_display_var,
            width=40,
            font=ctk.CTkFont(weight="bold")
        ).pack(side="right", padx=10)
        
        self.temperature_slider = ctk.CTkSlider(
            temp_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            variable=self.temperature_var,
            command=self.update_temperature_label
        )
        self.temperature_slider.pack(side="right", padx=10, fill="x", expand=True)
        
        tokens_frame = ctk.CTkFrame(tab)
        tokens_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(tokens_frame, text="Макс. токенов:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            tokens_frame,
            values=self.max_tokens_options,
            variable=self.max_tokens_var,
            width=120
        ).pack(side="right", padx=10)
        
        # Ensure label is in sync with slider value
        self.update_temperature_label(self.temperature_var.get())
    
    def _build_interface_tab(self, tab):
        ctk.CTkLabel(tab, text="Настройки интерфейса", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 12))
        
        theme_frame = ctk.CTkFrame(tab)
        theme_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(theme_frame, text="Тема:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            theme_frame,
            values=["light", "dark", "system"],
            variable=self.theme_var,
            width=150
        ).pack(side="right", padx=10)
        
        scale_frame = ctk.CTkFrame(tab)
        scale_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(scale_frame, text="Масштаб интерфейса:").pack(side="left", padx=10)
        ctk.CTkComboBox(
            scale_frame,
            values=list(self.ui_scale_map.keys()),
            variable=self.ui_scale_choice_var,
            width=150
        ).pack(side="right", padx=10)
        
        ai_panel_frame = ctk.CTkFrame(tab)
        ai_panel_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(ai_panel_frame, text="Показывать панель AI:").pack(side="left", padx=10)
        ctk.CTkSwitch(ai_panel_frame, text="", variable=self.show_ai_panel_var).pack(side="right", padx=10)
        
        statusbar_frame = ctk.CTkFrame(tab)
        statusbar_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(statusbar_frame, text="Показывать строку состояния:").pack(side="left", padx=10)
        ctk.CTkSwitch(statusbar_frame, text="", variable=self.show_statusbar_var).pack(side="right", padx=10)
    
    def _build_actions(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="transparent",
            border_width=1,
            width=120
        ).pack(side="left", padx=6)
        
        ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            command=self.save_settings,
            width=140
        ).pack(side="right", padx=6)
    
    def toggle_api_visibility(self):
        if self.show_api_var.get():
            self.api_entry.configure(show="*")
            self.api_toggle_btn.configure(text="Показать")
            self.show_api_var.set(False)
        else:
            self.api_entry.configure(show="")
            self.api_toggle_btn.configure(text="Скрыть")
            self.show_api_var.set(True)
    
    def update_temperature_label(self, value):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            numeric_value = 0.7
        self.temperature_display_var.set(f"{numeric_value:.1f}")
        if abs(self.temperature_var.get() - numeric_value) > 1e-6:
            self.temperature_var.set(numeric_value)
    
    def save_settings(self):
        if not self.config.has_section('INTERFACE'):
            self.config.add_section('INTERFACE')
        if not self.config.has_section('AI_SETTINGS'):
            self.config.add_section('AI_SETTINGS')
        if not self.config.has_section('API'):
            self.config.add_section('API')
        if not self.config.has_section('EDITOR'):
            self.config.add_section('EDITOR')
        
        self.config.set('EDITOR', 'default_font', self.font_var.get())
        self.config.set('EDITOR', 'default_font_size', self.size_var.get())
        self.config.set('EDITOR', 'autosave_interval', self.autosave_var.get())
        
        self.config.set('API', 'gemini_api_key', self.api_var.get())
        self.config.set('AI_SETTINGS', 'model', self.model_var.get())
        self.config.set('AI_SETTINGS', 'temperature', f"{self.temperature_var.get():.1f}")
        self.config.set('AI_SETTINGS', 'max_tokens', self.max_tokens_var.get())
        
        scale_value = self.ui_scale_map.get(self.ui_scale_choice_var.get(), '1.0')
        self.config.set('INTERFACE', 'theme', self.theme_var.get())
        self.config.set('INTERFACE', 'ui_scale', scale_value)
        self.config.set('INTERFACE', 'show_ai_panel', str(self.show_ai_panel_var.get()))
        self.config.set('INTERFACE', 'show_statusbar', str(self.show_statusbar_var.get()))
        
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
