import asyncio
import logging
from aiogram import Bot, types, Dispatcher, executor
from menu import Menu
TOKEN = "6926639788:AAHjaj9gKNBWMiFeoCqmxl_pCyrp2mwBD-o"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = Menu()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply(f'''Привет, я бот для парсинга сайта cubemarket.ru\n
Комманды:
/sales - вывести кубики рубика по скидке\n
/info - информация о боте\n
/max - получить кубик рубика максимальной стоимости\n
/new - вывести новинки''')
    
@dp.message_handler(commands=['info'])
async def info(msg: types.Message):
    await msg.reply(f'Автор: Александров Андрей, бот создан для код ревью')

@dp.message_handler(commands=['max'])
async def max_cube(msg: types.Message):
    await msg.reply(menu.get_max_cube())

@dp.message_handler(commands=['sales'])
async def get_sales(msg: types.Message):
    sale = menu.get_sales()
    await msg.answer(f'''Вывожу акции по кубикам рубика: 
{sale}''')

@dp.message_handler(commands=['new'])
async def info(msg: types.Message):
    await msg.reply(menu.get_new())


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    pass

if __name__ == '__main__':
    menu.refresh_information_about_cubes()
    executor.start_polling(dp)