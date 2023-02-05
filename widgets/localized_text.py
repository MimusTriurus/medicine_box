from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.when import WhenCondition

from constants import LANG, EN, START_DATA


class LocalizedText(Text):
    def __init__(self, text_maker, when: WhenCondition = None):
        super().__init__(when)
        self.text_maker = text_maker

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        current_lang = data[START_DATA][LANG] if data[START_DATA] else EN
        return self.text_maker(current_lang)
