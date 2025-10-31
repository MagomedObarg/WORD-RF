#!/usr/bin/env python3
"""
AI Text Editor - Gemini
Современный текстовый редактор с AI-ассистентом на базе Google Gemini

Автор: AI Text Editor Team
Версия: 1.0.0
"""

import sys
import logging
from editor import TextEditor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting AI Text Editor")
        app = TextEditor()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
