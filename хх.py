from telegram.ext import Application, MessageHandler, filters
from config import TOKEN_API
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
import datetime
from random import randint

reply_keyboard = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )


async def dice_command(update, context):
    reply_keyboard = [['/dice 1d6', '/dice 2d6'], ['/dice 1d20', '/start']]
    dice_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    if update.message.text.replace("/dice", "") and update.message.text.replace("/dice", "") != '/start':
        data = update.message.text.replace("/dice ", "")
        print(data.split('d'))
        await update.message.reply_text(
            ' '.join([str(randint(1, int(data.split('d')[-1]))) for _ in range(int(data.split('d')[0]))]))
    await update.message.reply_text(
        "Какой кубик будем кидать?",
        reply_markup=dice_markup
    )

    print(update.message.reply_markup)


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


# Обычный обработчик, как и те, которыми мы пользовались раньше.
async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, int(update.message.text.replace("/set ", "")), chat_id=chat_id, name=str(chat_id),
                               data=int(update.message.text.replace("/set ", "")))

    text = f'Вернусь через {int(update.message.text.replace("/set ", ""))} с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {context.job.data}c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token(TOKEN_API).build()

    # Регистрируем обработчик в приложении.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("dice", dice_command))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
