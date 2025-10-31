import google.generativeai as genai
import threading
import logging
from typing import Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAssistant:
    def __init__(self, api_key: str, model_name: str = "gemini-pro", temperature: float = 0.7):
        self.api_key = (api_key or "").strip()
        self.model_name = model_name.strip() if isinstance(model_name, str) and model_name.strip() else "gemini-pro"
        self.temperature = temperature
        self.model = None
        self.chat_history = []
        self.is_configured = False
        
        # Validate API key more strictly
        if self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.is_configured = True
                logger.info("AI Assistant initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI Assistant: {e}")
                self.is_configured = False
        else:
            logger.warning("AI Assistant not configured: Invalid or missing API key")
    
    def is_ready(self) -> bool:
        return self.is_configured and self.model is not None
    
    def generate_async(self, prompt: str, callback: Callable[[str, Optional[str]], None]):
        if not self.is_ready():
            error_msg = "AI Assistant is not properly configured"
            logger.error(error_msg)
            callback("", error_msg)
            return
        
        def task():
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                    )
                )
                result = response.text
                self.chat_history.append({"prompt": prompt, "response": result})
                callback(result, None)
            except Exception as e:
                error_msg = f"AI Error: {str(e)}"
                logger.error(error_msg)
                callback("", error_msg)
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
    
    def improve_text(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Улучши следующий текст, сделав его более читаемым, грамотным и профессиональным. 
Сохрани исходный смысл и язык текста:

{text}

Верни только улучшенный текст без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def rewrite_text(self, text: str, style: str, callback: Callable[[str, Optional[str]], None]):
        styles = {
            "formal": "формальном деловом",
            "informal": "неформальном дружеском",
            "business": "деловом профессиональном",
            "creative": "творческом креативном",
            "academic": "академическом научном"
        }
        style_desc = styles.get(style, "нейтральном")
        
        prompt = f"""Перепиши следующий текст в {style_desc} стиле. 
Сохрани основную мысль, но измени формулировки:

{text}

Верни только переписанный текст без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def continue_text(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Продолжи следующий текст логичным и связным образом. 
Напиши следующий абзац или несколько предложений:

{text}

Верни только продолжение текста без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def fix_grammar(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Исправь все грамматические, орфографические и пунктуационные ошибки в следующем тексте:

{text}

Верни только исправленный текст без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def shorten_text(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Сократи следующий текст, сохранив ключевые моменты и основной смысл:

{text}

Верни только сокращенный текст без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def expand_text(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Расширь следующий текст, добавив больше деталей, примеров и объяснений:

{text}

Верни только расширенный текст без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def translate_text(self, text: str, target_language: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Переведи следующий текст на {target_language}:

{text}

Верни только перевод без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def summarize_text(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Создай краткое резюме следующего текста, выделив главные идеи:

{text}

Верни только резюме без дополнительных комментариев."""
        self.generate_async(prompt, callback)
    
    def generate_document(self, doc_type: str, description: str, callback: Callable[[str, Optional[str]], None]):
        templates = {
            "letter": "деловое письмо",
            "resume": "резюме",
            "contract": "договор",
            "report": "отчет",
            "article": "статью"
        }
        doc_desc = templates.get(doc_type, "документ")
        
        prompt = f"""Создай {doc_desc} на основе следующего описания:

{description}

Создай полный, структурированный и профессиональный документ."""
        self.generate_async(prompt, callback)
    
    def answer_question(self, question: str, context: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""На основе следующего контекста ответь на вопрос:

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

Дай развернутый и точный ответ на основе предоставленного контекста."""
        self.generate_async(prompt, callback)
    
    def generate_headlines(self, text: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Проанализируй следующий текст и предложи структуру с заголовками:

{text}

Верни только список заголовков с краткими описаниями разделов."""
        self.generate_async(prompt, callback)
    
    def chat(self, message: str, callback: Callable[[str, Optional[str]], None]):
        prompt = f"""Ты - помощник в текстовом редакторе. Помоги пользователю с его запросом:

{message}

Дай полезный и конкретный ответ."""
        self.generate_async(prompt, callback)
    
    def get_chat_history(self):
        return self.chat_history
    
    def clear_history(self):
        self.chat_history.clear()
