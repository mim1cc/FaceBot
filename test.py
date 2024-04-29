import os
from telegram_secrets import TOKEN_API
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler()
async def message_wait(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f"Я получил сообщение {message.text}")


if __name__ == '__main__':
    executor.start_polling(dp)
