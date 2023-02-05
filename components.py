from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

storage: MemoryStorage = MemoryStorage()
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=storage)
