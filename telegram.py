import asyncio
import threading
from aiogram import Bot, Dispatcher, types, executor
import credentials
import vfs_parser


bot = Bot(credentials.telegram_token)
dispatcher = Dispatcher(bot)
parser_task: asyncio.Task = None
shutdown_event = threading.Event()


@dispatcher.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply('Parser started to work!')
    shutdown_event.clear()
    global parser_task
    parser_coro = asyncio.to_thread(vfs_parser.main, shutdown_event)
    parser_task = asyncio.create_task(parser_coro)


@dispatcher.message_handler(commands=['shutdown'])
async def shutdown(msg: types.Message):
    shutdown_event.set()
    await parser_task
    await msg.reply('Shut down successfully')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
