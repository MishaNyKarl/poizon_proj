import requests
from bs4 import BeautifulSoup
from aiogram.types import InputFile
from datetime import datetime
from aiogram.types import ChatActions
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт MemoryStorage
import logging
import asyncio
import asyncio
import logging
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import asyncio
import redis
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6380874791:AAHu--ztTOsFvtkY3xqPEdXwvK80N5VnyfQ")
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

storage = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class DrugoeState(StatesGroup):
    waiting_for_drugoe_price = State()
    waiting_for_drugoe_weight = State()


class UserState(StatesGroup):
    waiting_for_shmot_price = State()


# Хэндлер на команду /start
@dp.message_handler(Command("start"), state="*")
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Гайд по приложению Poizon 📃"),
            types.KeyboardButton(text="Отзывы наших клиентов 📒")
        ],
        [
            types.KeyboardButton(text="Актуальные курсы ¥ и $ 📈"),
            types.KeyboardButton(text="Наши соц. сети 💻")
        ],
        [
            types.KeyboardButton(text="Рассчитать цену товара 💴"),
            types.KeyboardButton(text="Оформить заказ 👨🏻‍💻")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Стартовое меню"
    )
    await message.answer('Привет, я Бот канала <a href="https://t.me/sneakerspot1">SNEAKER SPOT</a>! 👟 \n\nЯ создан с целью сбора всей полезной информации, а также вопросов, которые могут возникнуть при заказе с китайской торговой площадки.🤖', reply_markup=keyboard, parse_mode="HTML")


# Используем правильный импорт и фильтр Text
@dp.message_handler(Text(equals="Гайд по приложению Poizon 📃"))
async def gaid(message: types.Message):

    # last_bot_message_id = last_bot_messages.get(message.chat.id)
    # if last_bot_message_id:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    #
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    guide_link = "https://telegra.ph/Gajd-po-prilozheniyu-Poizon-08-15"

    keyboard = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton(text="Откройте гайд по приложению Poizon", url=guide_link)
    keyboard.add(link_button)
    with open('poiz.jpg', 'rb') as photo:
        photo = InputFile(photo)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Специально для Вас мы подготовили статью, в которой рассказали про все детали и нюансы приложения Poizon, в том числе и рассказали, как зарегистрироваться на этой торговой площадке 👇", reply_markup=keyboard)




@dp.message_handler(Text(equals="Отзывы наших клиентов 📒"))
async def open_reviews(message: types.Message):
    reviews_link = "https://t.me/feedbacksneakerspot1"

    # Удаление предыдущего сообщения бота (если есть)
    # last_bot_message_id = last_bot_messages.get(message.chat.id)
    # if last_bot_message_id:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    #
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Создаем кнопку-гиперссылку
    keyboard = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton(text="Откройте отзывы наших клиентов", url=reviews_link)
    keyboard.add(link_button)

    sent_message = await bot.send_message(chat_id=message.chat.id,
                                          text="Вы можете посмотреть отзывы наших клиентов по ссылке:",
                                          reply_markup=keyboard)

    # Сохраняем идентификатор последнего сообщения бота
    # last_bot_messages[message.chat.id] = sent_message.message_id


@dp.message_handler(Text(equals="Актуальные курсы ¥ и $ 📈"))
async def kurs(message: types.Message):

    # last_bot_message_id = last_bot_messages.get(message.chat.id)
    # if last_bot_message_id:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    #
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    sent_message = await bot.send_message(chat_id=message.chat.id,
                                          text="Секунду, загружаются курсы...")

    url_dollar = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBgUqRgQt9Lg-ktQi2mwNk3uJzxFQg%3A1692141647367&ei=TwjcZNmIFoaawPAPtNaL0Aw&ved=0ahUKEwiZ7LPu5t-AAxUGDRAIHTTrAsoQ4dUDCA8&uact=5&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lp=Egxnd3Mtd2l6LXNlcnAiJdC60YPRgNGBINC00L7Qu9C70LDRgNCwINC6INGA0YPQsdC70Y4yEBAAGIAEGLEDGIMBGEYYggIyCxAAGIAEGLEDGIMBMgsQABiABBixAxiDATILEAAYgAQYsQMYgwEyCBAAGIAEGLEDMgsQABiABBixAxiDATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIuzBQpQJYnC5wBHgBkAEAmAHhAaAB2h6qAQYwLjIyLjG4AQPIAQD4AQGoAhTCAgcQIxjqAhgnwgIWEC4YAxiPARjqAhi0AhiMAxjlAtgBAcICFhAAGAMYjwEY6gIYtAIYjAMY5QLYAQHCAgcQIxiKBRgnwgILEC4YgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICBxAAGIoFGEPCAg0QLhiKBRixAxiDARhDwgIHEC4YigUYQ8ICDRAAGIoFGLEDGIMBGEPCAgUQLhiABMICBBAjGCfCAhAQABiKBRixAxiDARjJAxhDwgIIEAAYigUYkgPCAgoQABiKBRjJAxhD4gMEGAAgQYgGAboGBggBEAEYCw&sclient=gws-wiz-serp"  # Замените на реальный URL для курса доллара
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
    url_yuan = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBiCHC9hllmlUGu3GfOL1klsBV5_PA%3A1692141655066&ei=VwjcZL3aA_S_wPAPsqyb4Ao&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%BB&gs_lp=Egxnd3Mtd2l6LXNlcnAiG9C60YPRgNGBINGO0LDQvdC4INC6INGA0YPQuyoCCAAyDBAAGA0YgAQYRhiCAjIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkiZOVDRBljQJnABeAGQAQCYAbQBoAGFE6oBBDAuMTW4AQHIAQD4AQGoAhTCAgcQIxjqAhgnwgIQEAAYigUY6gIYtAIYQ9gBAcICBxAjGIoFGCfCAgQQIxgnwgIQEAAYgAQYFBiHAhixAxiDAcICCxAAGIAEGLEDGIMBwgILEAAYigUYsQMYgwHCAg0QABiKBRixAxiDARhDwgIHEAAYigUYQ8ICDBAjGIoFGCcYRhiCAsICDRAAGIAEGBQYhwIYsQPCAgoQABiABBgUGIcCwgIFEAAYgATCAg8QABiABBgUGIcCGEYYggLiAwQYACBBiAYBugYGCAEQARgB&sclient=gws-wiz-serp"  # Замените на реальный URL для курса юаня

    response_dollar = requests.get(url_dollar,headers=headers)
    response_yuan = requests.get(url_yuan, headers=headers)

    soup_dollar = BeautifulSoup(response_dollar.text, "html.parser")
    soup_yuan = BeautifulSoup(response_yuan.text, "html.parser")

    dollar_rate = soup_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',','.')
    yuan_rate = soup_yuan.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',','.')

    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")
    with open('kurs.jpg', 'rb') as photo:
        photo = InputFile(photo)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"Актуальный курс на {formatted_datetime}: ⌚️\n\n"

                            f"$ (USD) - {round(float(dollar_rate), 1)} ₽\n"
                            f"¥ (CNY) - {round(float(yuan_rate) + 0.7, 1)} ₽")
    # await message.answer(f"Актуальный курс на {formatted_datetime}: ⌚️\n"
    #
    #                         f"$ (USD) - {round(float(dollar_rate), 1)} ₽\n"
    #                         f"¥ (CNY) - {round(float(yuan_rate) + 0.7, 1)} ₽")

    # last_bot_messages[message.chat.id] = sent_message.message_id


@dp.message_handler(Text(equals="Наши соц. сети 💻"))
async def social_media(message: types.Message):
    telegram_link = 'https://t.me/sneakerspot1'
    inst_link = 'https://instagram.com/sneakerspot_only1?igshid=MjEwN2IyYWYwYw=='

    keyboard = types.InlineKeyboardMarkup()
    link_button_tel = types.InlineKeyboardButton(text="Наш телеграм", url=telegram_link)
    link_button_vk = types.InlineKeyboardButton(text="Наш инстаграм", url=inst_link)
    keyboard.add(link_button_tel, link_button_vk)

    await message.answer("Вы можете посмотреть отзывы наших клиентов, нажав на кнопку:", reply_markup=keyboard)


@dp.message_handler(Text(equals="Рассчитать цену товара 💴"))
async def product_price(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Обувь"),
            types.KeyboardButton(text="Верхняя одежда")
        ],
        [
            types.KeyboardButton(text="Толстовки/штаны"),
            types.KeyboardButton(text="Футболки/шорты")
        ],
        [
            types.KeyboardButton(text="Носки/нижнее белье"),
            types.KeyboardButton(text="Сумки")
        ],
        [
            types.KeyboardButton(text="Другое"),
            types.KeyboardButton(text="Вернуться назад")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Меню товара"
    )
    await message.answer(
        'Выберите категорию товара',
        reply_markup=keyboard, parse_mode="HTML")
    await DrugoeState.waiting_for_drugoe_price.set()




@dp.message_handler(Text(equals="Обувь"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Обувь'
    massa = 1200
    kit_com = 350
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(Text(equals="Верхняя одежда"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Верхняя одежда'
    massa = 1300
    kit_com = 350
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(Text(equals="Толстовки/штаны"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Толстовки/штаны'
    massa = 1000
    kit_com = 250
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(Text(equals="Футболки/шорты"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Футболки/шорты'
    massa = 600
    kit_com = 250
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(Text(equals="Носки/нижнее белье"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Носки/нижнее белье'
    massa = 250
    kit_com = 250
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(Text(equals="Сумки"), state="*")
async def enter_shoe_price(message: types.Message, state: FSMContext):
    but = 'Сумки'
    massa = 1250
    kit_com = 350
    await state.update_data(massa=massa, kit_com=kit_com)
    await message.answer(f"Введите стоимость {but} в юанях:")
    await UserState.waiting_for_shmot_price.set()

@dp.message_handler(lambda message: message.text.isdigit(), state=UserState.waiting_for_shmot_price)
async def process_shmot_price(message: types.Message, state: FSMContext):
    try:
        price = round(float(str(message.text)))
        print(price)
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')

    if price >= 1000:
        com = 50
    elif price >= 500:
        com = 30
    elif price < 500:
        com = 20



    # Получите сохраненную цену из состояния
    data = await state.get_data()
    massa = data.get('massa')
    kit_com = data.get('kit_com')

    # Вычислите общую стоимость (цена * вес)


    kb = [
        [
            types.KeyboardButton(text="Гайд по приложению Poizon 📃"),
            types.KeyboardButton(text="Отзывы наших клиентов 📒")
        ],
        [
            types.KeyboardButton(text="Актуальные курсы ¥ и $ 📈"),
            types.KeyboardButton(text="Наши соц. сети 💻")
        ],
        [
            types.KeyboardButton(text="Рассчитать цену товара 💴"),
            types.KeyboardButton(text="Оформить заказ 👨🏻‍💻")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Стартовое меню"
    )



    url_dollar = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBgUqRgQt9Lg-ktQi2mwNk3uJzxFQg%3A1692141647367&ei=TwjcZNmIFoaawPAPtNaL0Aw&ved=0ahUKEwiZ7LPu5t-AAxUGDRAIHTTrAsoQ4dUDCA8&uact=5&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lp=Egxnd3Mtd2l6LXNlcnAiJdC60YPRgNGBINC00L7Qu9C70LDRgNCwINC6INGA0YPQsdC70Y4yEBAAGIAEGLEDGIMBGEYYggIyCxAAGIAEGLEDGIMBMgsQABiABBixAxiDATILEAAYgAQYsQMYgwEyCBAAGIAEGLEDMgsQABiABBixAxiDATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIuzBQpQJYnC5wBHgBkAEAmAHhAaAB2h6qAQYwLjIyLjG4AQPIAQD4AQGoAhTCAgcQIxjqAhgnwgIWEC4YAxiPARjqAhi0AhiMAxjlAtgBAcICFhAAGAMYjwEY6gIYtAIYjAMY5QLYAQHCAgcQIxiKBRgnwgILEC4YgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICBxAAGIoFGEPCAg0QLhiKBRixAxiDARhDwgIHEC4YigUYQ8ICDRAAGIoFGLEDGIMBGEPCAgUQLhiABMICBBAjGCfCAhAQABiKBRixAxiDARjJAxhDwgIIEAAYigUYkgPCAgoQABiKBRjJAxhD4gMEGAAgQYgGAboGBggBEAEYCw&sclient=gws-wiz-serp"  # Замените на реальный URL для курса доллара
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
    url_yuan = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBiCHC9hllmlUGu3GfOL1klsBV5_PA%3A1692141655066&ei=VwjcZL3aA_S_wPAPsqyb4Ao&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%BB&gs_lp=Egxnd3Mtd2l6LXNlcnAiG9C60YPRgNGBINGO0LDQvdC4INC6INGA0YPQuyoCCAAyDBAAGA0YgAQYRhiCAjIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkiZOVDRBljQJnABeAGQAQCYAbQBoAGFE6oBBDAuMTW4AQHIAQD4AQGoAhTCAgcQIxjqAhgnwgIQEAAYigUY6gIYtAIYQ9gBAcICBxAjGIoFGCfCAgQQIxgnwgIQEAAYgAQYFBiHAhixAxiDAcICCxAAGIAEGLEDGIMBwgILEAAYigUYsQMYgwHCAg0QABiKBRixAxiDARhDwgIHEAAYigUYQ8ICDBAjGIoFGCcYRhiCAsICDRAAGIAEGBQYhwIYsQPCAgoQABiABBgUGIcCwgIFEAAYgATCAg8QABiABBgUGIcCGEYYggLiAwQYACBBiAYBugYGCAEQARgB&sclient=gws-wiz-serp"  # Замените на реальный URL для курса юаня

    response_dollar = requests.get(url_dollar, headers=headers)
    response_yuan = requests.get(url_yuan, headers=headers)

    soup_dollar = BeautifulSoup(response_dollar.text, "html.parser")
    soup_yuan = BeautifulSoup(response_yuan.text, "html.parser")

    dollar_rate = soup_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',', '.')
    yuan_rate = soup_yuan.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',', '.')

    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")

    dollar_kurs = round(float(dollar_rate), 1)
    yuan_kurs = round(float(yuan_rate) + 0.7, 1)

    if 50000 < (yuan_kurs * price):
        our_com = yuan_kurs * price * 0.06
    elif 30000 < (yuan_kurs * price) < 49999:
        our_com = yuan_kurs * price * 0.07
    elif 25000 < (yuan_kurs * price) < 29999:
        our_com = yuan_kurs * price * 0.08
    elif 15000 < (yuan_kurs * price) < 24999:
        our_com = yuan_kurs * price * 0.09
    elif 10000 < (yuan_kurs * price) < 14999:
        our_com = yuan_kurs * price * 0.10
    elif (yuan_kurs * price) < 9999:
        our_com = 1000



    total_price = (price * round(float(yuan_rate) + 0.7, 1)) + (our_com)  + ((massa/1000)*26*yuan_kurs) + (com * round(float(yuan_rate) + 0.7, 1)) + (kit_com)
    await message.answer(f"Конечная стоимость товара = {round(total_price)} ₽\n\n"
                         f"Актуальный курс на {formatted_datetime}: ⌚️\n\n"

                         f"$ (USD) - {round(float(dollar_rate), 1)} ₽\n"
                         f"¥ (CNY) - {round(float(yuan_rate) + 0.7, 1)} ₽\n\n"
                         f"❓Что включает в себя стоимость товара❓\n\n"
                         f"Стоимость товара на Poizon с учетом актуального курса - {round((price * round(float(yuan_rate) + 0.7, 1)),5)} ₽\n"
                         f"Наша комиссия - {round(our_com)} ₽\n"
                         f"Доставка по Китаю - {kit_com} ₽\n"
                         f"Доставка из Китая в Москву ≈ {round(((massa/1000)*26*yuan_kurs),5)} ₽\n"
                         f"Комиссия нашего посредника из Китая - {com * round(float(yuan_rate) + 0.7, 1)} ₽", reply_markup=keyboard)




    # Завершите состояние, чтобы пользователь мог снова выбирать товар
    await state.finish()





@dp.message_handler(Text(equals="Другое"), state="*")
async def enter_drugoe_massa(message: types.Message):
    await message.answer("❗️Введите вес товара, который хотите заказать в граммах. Вес может быть примерным, смотрите в интернете❗️")
    await DrugoeState.waiting_for_drugoe_weight.set()

@dp.message_handler(lambda message: message.text.isdigit(), state=DrugoeState.waiting_for_drugoe_weight)
async def massa_drugoe(message: types.Message, state: DrugoeState):
    massa = int(message.text)
    kit_com = 450
    await message.answer(f"Введенный вес: {massa} грамм", parse_mode=ParseMode.MARKDOWN)

    await state.update_data(massa=massa, kit_com=kit_com)

    await message.answer(f"Введите цену в юанях:")
    await DrugoeState.waiting_for_drugoe_price.set()

@dp.message_handler(lambda message: message.text.isdigit(), state=DrugoeState.waiting_for_drugoe_price)
async def process_drugoe_price(message: types.Message, state: FSMContext):
    try:
        price = round(float(str(message.text)))
        print(price)
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')

    if price >= 1000:
        com = 50
    elif price >= 500:
        com = 30
    elif price < 500:
        com = 20

    # Получите сохраненную цену из состояния
    data = await state.get_data()
    massa = data.get('massa')
    kit_com = data.get('kit_com')


    kb = [
        [
            types.KeyboardButton(text="Гайд по приложению Poizon 📃"),
            types.KeyboardButton(text="Отзывы наших клиентов 📒")
        ],
        [
            types.KeyboardButton(text="Актуальные курсы ¥ и $ 📈"),
            types.KeyboardButton(text="Наши соц. сети 💻")
        ],
        [
            types.KeyboardButton(text="Рассчитать цену товара 💴"),
            types.KeyboardButton(text="Оформить заказ 👨🏻‍💻")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Стартовое меню"
    )
    url_dollar = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBgUqRgQt9Lg-ktQi2mwNk3uJzxFQg%3A1692141647367&ei=TwjcZNmIFoaawPAPtNaL0Aw&ved=0ahUKEwiZ7LPu5t-AAxUGDRAIHTTrAsoQ4dUDCA8&uact=5&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lp=Egxnd3Mtd2l6LXNlcnAiJdC60YPRgNGBINC00L7Qu9C70LDRgNCwINC6INGA0YPQsdC70Y4yEBAAGIAEGLEDGIMBGEYYggIyCxAAGIAEGLEDGIMBMgsQABiABBixAxiDATILEAAYgAQYsQMYgwEyCBAAGIAEGLEDMgsQABiABBixAxiDATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIuzBQpQJYnC5wBHgBkAEAmAHhAaAB2h6qAQYwLjIyLjG4AQPIAQD4AQGoAhTCAgcQIxjqAhgnwgIWEC4YAxiPARjqAhi0AhiMAxjlAtgBAcICFhAAGAMYjwEY6gIYtAIYjAMY5QLYAQHCAgcQIxiKBRgnwgILEC4YgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICBxAAGIoFGEPCAg0QLhiKBRixAxiDARhDwgIHEC4YigUYQ8ICDRAAGIoFGLEDGIMBGEPCAgUQLhiABMICBBAjGCfCAhAQABiKBRixAxiDARjJAxhDwgIIEAAYigUYkgPCAgoQABiKBRjJAxhD4gMEGAAgQYgGAboGBggBEAEYCw&sclient=gws-wiz-serp"  # Замените на реальный URL для курса доллара
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
    url_yuan = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sca_esv=557255143&sxsrf=AB5stBiCHC9hllmlUGu3GfOL1klsBV5_PA%3A1692141655066&ei=VwjcZL3aA_S_wPAPsqyb4Ao&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D0%B8+%D0%BA+%D1%80%D1%83%D0%BB&gs_lp=Egxnd3Mtd2l6LXNlcnAiG9C60YPRgNGBINGO0LDQvdC4INC6INGA0YPQuyoCCAAyDBAAGA0YgAQYRhiCAjIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkiZOVDRBljQJnABeAGQAQCYAbQBoAGFE6oBBDAuMTW4AQHIAQD4AQGoAhTCAgcQIxjqAhgnwgIQEAAYigUY6gIYtAIYQ9gBAcICBxAjGIoFGCfCAgQQIxgnwgIQEAAYgAQYFBiHAhixAxiDAcICCxAAGIAEGLEDGIMBwgILEAAYigUYsQMYgwHCAg0QABiKBRixAxiDARhDwgIHEAAYigUYQ8ICDBAjGIoFGCcYRhiCAsICDRAAGIAEGBQYhwIYsQPCAgoQABiABBgUGIcCwgIFEAAYgATCAg8QABiABBgUGIcCGEYYggLiAwQYACBBiAYBugYGCAEQARgB&sclient=gws-wiz-serp"  # Замените на реальный URL для курса юаня

    response_dollar = requests.get(url_dollar, headers=headers)
    response_yuan = requests.get(url_yuan, headers=headers)

    soup_dollar = BeautifulSoup(response_dollar.text, "html.parser")
    soup_yuan = BeautifulSoup(response_yuan.text, "html.parser")

    dollar_rate = soup_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',', '.')
    yuan_rate = soup_yuan.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})[0].text.replace(',', '.')

    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")

    dollar_kurs = round(float(dollar_rate), 1)
    yuan_kurs = round(float(yuan_rate) + 0.7, 1)

    if 50000 < (yuan_kurs * price):
        our_com = yuan_kurs * price * 0.06
    elif 30000 < (yuan_kurs * price) < 49999:
        our_com = yuan_kurs * price * 0.07
    elif 25000 < (yuan_kurs * price) < 29999:
        our_com = yuan_kurs * price * 0.08
    elif 15000 < (yuan_kurs * price) < 24999:
        our_com = yuan_kurs * price * 0.09
    elif 10000 < (yuan_kurs * price) < 14999:
        our_com = yuan_kurs * price * 0.10
    elif (yuan_kurs * price) < 9999:
        our_com = 1000

    total_price = (price * round(float(yuan_rate) + 0.7, 1)) + (our_com) + ((massa / 1000) * 26 * yuan_kurs) + (com * round(float(yuan_rate) + 0.7, 1)) + float(kit_com)
    await message.answer(f"Конечная стоимость товара = {round(total_price)} ₽\n\n"
                         f"Актуальный курс на {formatted_datetime}: ⌚️\n\n"

                         f"$ (USD) - {round(float(dollar_rate), 1)} ₽\n"
                         f"¥ (CNY) - {round(float(yuan_rate) + 0.7, 1)} ₽\n\n"
                         f"❓Что включает в себя стоимость товара❓\n\n"
                         f"Стоимость товара на Poizon с учетом актуального курса - {round((price * round(float(yuan_rate) + 0.7, 1)), 5)} ₽\n"
                         f"Наша комиссия - {round(our_com)} ₽\n"
                         f"Доставка по Китаю - \n"
                         f"Доставка из Китая в Москву ≈ {round(((massa / 1000) * 26 * yuan_kurs), 5)} ₽\n"
                         f"Комиссия нашего посредника из Китая - {com * round(float(yuan_rate) + 0.7, 1)} ₽",
                         reply_markup=keyboard)

    # Завершите состояние, чтобы пользователь мог снова выбирать товар
    await state.finish()



@dp.message_handler(Text(equals="Вернуться назад"))
async def back(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Гайд по приложению Poizon 📃"),
            types.KeyboardButton(text="Отзывы наших 📒")
        ],
        [
            types.KeyboardButton(text="Актуальные курсы ¥ и $ 📈"),
            types.KeyboardButton(text="Наши соц. сети 💻")
        ],
        [
            types.KeyboardButton(text="Рассчитать цену товара 💴"),
            types.KeyboardButton(text="Оформить заказ 👨🏻‍💻")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Стартовое меню"
    )
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboard)


@dp.message_handler(Text(equals="Оформить заказ 👨🏻‍💻"))
async def we(message: types.Message):
    mok_link = 'https://t.me/Mokkkk'

    keyboard = types.InlineKeyboardMarkup()
    mok_link_but = types.InlineKeyboardButton(text="Написать продавцу", url=mok_link)

    keyboard.add(mok_link_but)

    await message.answer("Оформляем заказы круглосуточно, отвечаем достаточно быстро:", reply_markup=keyboard)







# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
