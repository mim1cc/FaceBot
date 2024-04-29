import os
from time import sleep
from config import PROGRESS_BAR_LEN, ANIMATION_LOADING
from telegram_secrets import TOKEN_API
from data.aliases import aliases
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.utils.exceptions import MessageNotModified

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def greet(name_key: str) -> list:
    pathes = []
    for file in os.listdir(rf"data/imgs/{name_key}"):
        pathes.append(os.path.join(f"data/imgs/{name_key}", file))
    return sorted(pathes, key=lambda p: int(p.split("\\")[-1][:-4]))


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=types.input_file.InputFile(r"data/imgs/system/celebration.jpg"),
                         caption='*Вас приветсвует терминал Матрицы №293009067*\n***Назначение узла***: Поздравление с 8 марта.\n' +
                                 'Для инициализации процесса, пожалуйста, введите свое имя: ', parse_mode="Markdown")


@dp.message_handler()
async def message_wait(message: types.Message):
    for key, value in aliases.items():
        if message["text"] in value:
            pathes = await greet(key)

            ready = 100 * 1 // len(pathes)
            cur = await bot.send_photo(chat_id=message.from_user.id,
                                       photo=types.input_file.InputFile(pathes[0]),
                                       caption=f'{(PROGRESS_BAR_LEN * ready // 100) * "█"} {(PROGRESS_BAR_LEN - (PROGRESS_BAR_LEN * ready // 100)) * "░"} {ready}% {ANIMATION_LOADING[0]}')
            for i, path in enumerate(pathes[1:]):
                ready = 100 * int(path.replace(".png", "").split("\\")[-1]) // len(pathes)
                cur = await bot.edit_message_media(
                    media=InputMediaPhoto(types.input_file.InputFile(path),
                                          caption=f'{(PROGRESS_BAR_LEN * ready // 100) * "█"} {(PROGRESS_BAR_LEN - (PROGRESS_BAR_LEN * ready // 100)) * "░"} {ready}% {ANIMATION_LOADING[i % len(ANIMATION_LOADING)]}'),
                    chat_id=message.from_user.id,
                    message_id=cur.message_id)
            else:
                cur = await bot.edit_message_media(
                    media=InputMediaPhoto(types.input_file.InputFile(pathes[-1]),
                                          caption=f"{'█' * PROGRESS_BAR_LEN} 100%\nПоздравляю с 1000⑵ марта!"),
                    chat_id=message.from_user.id,
                    message_id=cur.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
