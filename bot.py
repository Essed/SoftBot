from vkbottle.bot import Bot, Message
from config import Config, ConfigParser, Paginator
import csv
from autoutils import stringToList
from vkbottle import CtxStorage
from stockcontroller import StockData
from orderstorage import OrderStorage
from filters import hasWords
from users import UserSettings

bot = Bot(token=Config.TOKEN)
ctx = CtxStorage()

user_settings = UserSettings()
paginator = Paginator(10)
cfg_parser = ConfigParser()


@bot.on.message(text=["start", "начать"])
async def start(message: Message):
    await message.answer("Привет, на связи AutoSoft бот!")


@bot.on.message(text="кв <words>")
async def set_keywords(message: Message, words: str = None):
    words = words.split(' ')
    await user_settings.set_keywords(message.from_id, words)
    await message.answer("Выбраны ключевые фильтры")


@bot.on.message(text="cl")
async def clear_keywords(message: Message):
    await user_settings.set_keywords(message.from_id, list())
    await message.answer("Фильтр сброшен")


@bot.on.message(text="пг <count>")
async def set_pagination(message: Message, count: int = None):
    if count is not None:
        await paginator.set_pages(count)
        await message.answer(f"Заявок в выборке {count}")
    else:
        await message.answer(f"Стандартное количество заявок")


@bot.on.message(text="бр <name>")
async def set_stockmarket(message: Message, name: str = None):
    stock_name = "freelanceru"

    if name is not None:
        await cfg_parser.set_stock(name)
        await message.answer(f"Выбрана биржа {name}")
    else:
        await message.answer(f"Стандартная биржа {stock_name}")

    await bot.state_dispenser.set(message.peer_id, StockData.FIND)


@bot.on.message(text="еще", state=StockData.FIND)
async def show_next(message: Message):

    last_index = await OrderStorage.get_last_index()
    data_set = await OrderStorage.get_orders()

    pages = await paginator.get_pages()

    message_pack = ""
    iterator = 0

    if last_index % pages == 0 or last_index == len(data_set):
        await OrderStorage.set_index(0)

    if last_index + pages <= len(data_set):
        for index in range(last_index, last_index + pages):
            iterator += 1
            message_pack += (f"{iterator}. {data_set[index]}\n")

            if iterator == pages:
                await message.answer(message_pack)
                message_pack = ""
                last_index += iterator
                await OrderStorage.set_index(last_index)
                iterator = 0

    else:

        message_pack = ""
        tail = len(data_set) - last_index
        final = last_index + tail

        iterator = 0
        for index in range(last_index, final):
            iterator += 1
            message_pack += (f"{iterator}. {data_set[index]}\n")

            if index == final - 1:
                await OrderStorage.set_index(0)
                await message.answer(message_pack)


@bot.on.message(text="заявки")
async def orders(message: Message):

    await OrderStorage.set_index(0)
    await OrderStorage.set_orders("")

    path = await cfg_parser.get_stock()

    with open(path, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        lines = ""

        for row in reader:
            lines += f"{dict(row)['Название']} {dict(row)['Стоимость']}\n"

    data_set = await stringToList(lines.strip())

    keywords = await user_settings.user_keywords(message.from_id)

    if len(keywords) > 0:
        data_set = [data for data in data_set if await hasWords(data, keywords)]

    await OrderStorage.set_orders(data_set)

    pages = await paginator.get_pages()

    message_pack = ""

    iterator = 0
    if len(data_set) >= pages:
        for index in range(0, pages):
            iterator += 1
            message_pack += (f"{iterator}. {data_set[index]}\n")

            if iterator == pages:
                await message.answer(message_pack)
                await OrderStorage.set_main_orders(message_pack)
                message_pack = ""
                await OrderStorage.set_index(iterator)
                iterator = 0

        message_pack = ""

    else:
        for index in range(0, len(data_set)):
            iterator += 1
            message_pack += (f"{iterator}. {data_set[index]}\n")

            if index == len(data_set) - 1:
                await message.answer(message_pack)

                await OrderStorage.set_index(0)


@bot.on.message(text="кт <category>")
async def set_category(message: Message, category: str = None):
    category = category.split(' ')
    await user_settings.set_categories(message.from_id, category)
    await message.answer("Выбраны категории")


if __name__ == "__main__":
    bot.run_forever()
