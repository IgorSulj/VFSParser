import asyncio
import threading
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from aiogram import Bot, Dispatcher, types, executor
import credentials
import vfs_parser


def private_handler(func):
    async def handler(msg: types.Message):
        if msg.from_user['id'] in credentials.telegram_allowed_ids:
            await func(msg)

    return handler


shutdown_event = threading.Event()
bot = Bot(credentials.telegram_token)
dispatcher = Dispatcher(bot)
parser_task: asyncio.Task = None
notifier_task: asyncio.Task = None


async def notifier(msg: types.Message):
    try:
        await parser_task
        result = parser_task.result()
        if result is not None:
            await msg.reply(f'Нашел место в городе {result}')
    except NoSuchElementException:
        await msg.reply('Не смог найти нужный элемент...')
    except WebDriverException:
        await msg.reply('Что-то пошло не так в парсере...')


@dispatcher.message_handler(commands=['start', 'awake'])
@private_handler
async def start(msg: types.Message):
    global parser_task
    if parser_task is None or parser_task.done():
        shutdown_event.clear()
        parser_coro = asyncio.to_thread(vfs_parser.main, shutdown_event)
        parser_task = asyncio.create_task(parser_coro)
        await msg.reply('Парсер начал работу!')
        await notifier(msg)
    else:
        await msg.reply('Парсер уже работает')


@dispatcher.message_handler(commands=['shutdown'])
@private_handler
async def shutdown(msg: types.Message):
    if parser_task is not None and not parser_task.done():
        shutdown_event.set()
        await parser_task
        await msg.reply('Успешно завершил работу')
    else:
        await msg.reply('Парсер уже не работает')


@dispatcher.message_handler(commands=['info'])
@private_handler
async def info(msg: types.Message):
    parser_info = f'Статус: {"не работаю" if parser_task is None or parser_task.done() else "работаю"}'
    await msg.reply(parser_info)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
