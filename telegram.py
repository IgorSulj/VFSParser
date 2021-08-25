import asyncio
import threading
from functools import partial

from aiogram import Bot, Dispatcher, types, executor
import credentials
import vfs_parser


def private_handler(func):
    async def handler(msg: types.Message):
        if msg.from_user['id'] in credentials.telegram_allowed_ids:
            await func(msg)

    return handler


shutdown_event = threading.Event()
aio_shutdown_event = asyncio.Event()
bot = Bot(credentials.telegram_token)
dispatcher = Dispatcher(bot)
parser_task: asyncio.Task = None
notifier_task: asyncio.Task = None


async def notifier(msg: types.Message):
    done, pending = await asyncio.wait((parser_task, aio_shutdown_event.wait()), return_when=asyncio.FIRST_COMPLETED)
    if parser_task in done:
        await msg.reply(f'Нашел место в городе {parser_task.result()}')


@dispatcher.message_handler(commands=['start'])
@private_handler
async def start(msg: types.Message):
    global parser_task
    parser_coro = asyncio.to_thread(vfs_parser.main, shutdown_event)
    parser_task = asyncio.create_task(parser_coro)
    await msg.reply('Parser started to work!')
    await notifier(msg)


@dispatcher.message_handler(commands=['shutdown'])
@private_handler
async def shutdown(msg: types.Message):
    shutdown_event.set()
    aio_shutdown_event.set()
    await msg.reply('Shut down successfully')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
