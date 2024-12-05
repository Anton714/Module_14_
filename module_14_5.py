from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import initiate_db, get_all_products, is_included, add_user

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(input_field_placeholder='Выберите пункт меню.', resize_keyboard=True)

button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button)
kb.add(button2)
kb.add(button3)
kb.add(button4)

in_kb = InlineKeyboardMarkup()
in_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(in_button)
in_kb.add(in_button2)

products_all = get_all_products()

in2_kb = InlineKeyboardMarkup(resize_keyboard=True)
in2_button = InlineKeyboardButton(text=f'{products_all[0][0]}', callback_data='product_buying')
in2_button_2 = InlineKeyboardButton(text=f'{products_all[1][0]}', callback_data='product_buying')
in2_button_3 = InlineKeyboardButton(text=f'{products_all[2][0]}', callback_data='product_buying')
in2_button_4 = InlineKeyboardButton(text=f'{products_all[3][0]}', callback_data='product_buying')
in2_kb.insert(in2_button)
in2_kb.insert(in2_button_2)
in2_kb.insert(in2_button_3)
in2_kb.insert(in2_button_4)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('img (33).png', 'rb') as img:
        await message.answer_photo(img, f'Название: {products_all[0][0]} | Описание: {products_all[0][1]} | Цена: {products_all[0][2]} p')
    with open('img (37).png', 'rb') as img:
        await message.answer_photo(img, f'Название: {products_all[1][0]} | Описание: {products_all[1][1]} | Цена: {products_all[1][2]} p')
    with open('img (40).png', 'rb') as img:
        await message.answer_photo(img, f'Название: {products_all[2][0]} | Описание: {products_all[2][1]} | Цена: {products_all[2][2]} p')
    with open('img (49).png', 'rb') as img:
        await message.answer_photo(img, f'Название: {products_all[3][0]} | Описание: {products_all[3][1]} | Цена: {products_all[3][2]} p')
    await message.answer('Выберите продукт для покупки:', reply_markup=in2_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Информация'])
async def start_message(message):
    await message.answer('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.\n '
                         'Помогу рассчитать необходимое количество калорий в сутки')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (в пределах от 10 до 99 лет):')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    flag = False
    if len(message.text) == 2:
        flag = True
    num = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if flag and message.text[0] in num and message.text[1] in num and 9 < int(message.text) < 100:
        await message.answer('Введите свой рост (в пределах от 100 до 220 см):')
        await UserState.growth.set()
    else:
        await message.answer('Ввели некорректное значение, начнем заново.\n'
                             'Введите свой возраст (в пределах от 10 до 99 лет):')


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    flag = False
    if len(message.text) == 3:
        flag = True
    num = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if flag and message.text[0] in num and message.text[1] in num and message.text[2] in num and 99 < int(
            message.text) < 221:
        await message.answer('Введите свой вес (в пределах от 30 до 180 кг):')
        await UserState.weight.set()
    else:
        await message.answer('Ввели некорректное значение, начнем заново.\n'
                             'Введите свой рост (в пределах от 100 до 220 см):')


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    flag = False
    b = '0'
    if len(message.text) == 2:
        message.text = b + message.text

    if len(message.text) == 3:
        flag = True
        num = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if flag and message.text[0] in num and message.text[1] in num and message.text[2] in num and int and 29 < int(
            message.text) < 181:
        data = await state.get_data()
        res_men = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        res_women = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Необходимое количество килокалорий в сутки \n'
                             f'если вы мужчина: {res_men}, если женщина:  {res_women}')
        await state.finish()
    else:
        await message.answer('Ввели некорректное значение, начнем заново.\n'
                             'Введите свой вес (в пределах от 30 до 180 кг):')

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username_=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email_=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age_=message.text)
    data = await state.get_data()
    add_user(data['username_'], data['email_'], data['age_'])
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду: /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
