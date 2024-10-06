from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Токен бота
BOT_TOKEN = '6807340372:AAG0aXi2JwDkb1ewyxZax98iivmU_8GGHXs'  # Замените на ваш токен

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
survey_btn = KeyboardButton(text='Пройти опрос')
quiz1_btn = KeyboardButton(text='Викторина 1')
quiz2_btn = KeyboardButton(text='Викторина 2')


# Добавляем кнопки в билдер
kb_builder.row(survey_btn,quiz1_btn,quiz2_btn,width=2)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

# Опросные вопросы
survey_questions = [
    "Какой ваш любимый цвет?",
    "Какой ваш любимый сезон?",
    "Какой ваш любимый спорт?"
]
# Викторина 1
quiz1_questions=[
    "Кто написал 'Войну и мир'?",
    "Какая столица России?",
    "Сколько морей омывают Россию?"
]
quiz1_answers=[
    "Лев Толстой",
    "Москва",
    "15"
]
# Викторина 2
quiz2_questions=[
    "Сколько дней в году?",
    "Сколько месяцев в году?",
    "Сколько есть времен года?"
]
quiz2_answers=[
    "365",
    "12",
    "4"
]

# Переменные для хранения состояния пользователя
user_data = {}

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите, что хотите сделать:", reply_markup=keyboard)

# Обработчик кнопки "Пройти опрос"
@dp.message(lambda message: message.text == 'Пройти опрос')
async def start_survey(message: Message):
    user_data[message.from_user.id] = {"survey_step": 0, "survey_answers": []}
    await ask_survey_question(message)
async def ask_survey_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    question = survey_questions[step]
    await message.answer(question, reply_markup=types.ReplyKeyboardRemove())  # Убираем клавиатуру для ввода текста

@dp.message(lambda message: message.from_user.id in user_data and "survey_step" in user_data[message.from_user.id])
async def handle_survey_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    user_data[user_id]["survey_answers"].append(message.text)

    # Если есть еще вопросы
    if step + 1 < len(survey_questions):
        user_data[user_id]["survey_step"] += 1
        await ask_survey_question(message)
    else:
        # Выводим результаты опроса
        results = "\n".join(f"{q}: {a}" for q, a in zip(survey_questions, user_data[user_id]["survey_answers"]))
        await message.answer(f"Спасибо за участие в опросе!\nВаши ответы:\n{results}", reply_markup=keyboard)
        del user_data[user_id]  # Очищаем данные пользователя после завершения опроса

# Обработчик кнопки "Викторина 1"
@dp.message(lambda message: message.text == 'Викторина 1')
async def start_quiz1(message: Message):
    user_data[message.from_user.id] = {"quiz1_step": 0, "quiz1_score":0}
    await ask_quiz1_question(message)

async def ask_quiz1_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz1_step"]
    question = quiz1_questions[step]
    await message.answer(question, reply_markup=types.ReplyKeyboardRemove())  # Убираем клавиатуру для ввода текста

@dp.message(lambda message: message.from_user.id in user_data and "quiz1_step" in user_data[message.from_user.id])
async def handle_quiz1_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz1_step"]
    answer = message.text.strip().lower()

 # Приводим ответ к нижнему регистру

    if answer == quiz1_answers[step].lower():
        user_data[user_id]["quiz1_score"] += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {quiz1_answers[step]}")

    # Если есть еще вопросы
    if step + 1 < len(quiz1_questions):
        user_data[user_id]["quiz1_step"] += 1
        await ask_quiz1_question(message)
    else:
        # Выводим результат викторины
        score = user_data[user_id]["quiz1_score"]
        await message.answer(f"Викторина завершена! Вы ответили верно на {score} из {len(quiz1_questions)} вопросов.", reply_markup=keyboard)
        del user_data[user_id]  # Очищаем данные пользователя после завершения викторины

# Обработчик кнопки "Викторина 2"
@dp.message(lambda message: message.text == 'Викторина 2')
async def start_quiz2(message: Message):
    user_data[message.from_user.id] = {"quiz2_step": 0, "quiz2_score": 0}
    await ask_quiz2_question(message)

async def ask_quiz2_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz2_step"]
    question = quiz2_questions[step]
    await message.answer(question, reply_markup=types.ReplyKeyboardRemove())

@dp.message(lambda message: message.from_user.id in user_data and "quiz2_step" in user_data[message.from_user.id])
async def handle_quiz2_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz2_step"]
    answer = message.text.strip().lower()

    if answer == quiz2_answers[step].lower():
        user_data[user_id]["quiz2_score"] += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {quiz2_answers[step]}")

    # Если есть еще вопросы
    if step + 1 < len(quiz2_questions):
        user_data[user_id]["quiz2_step"] += 1
        await ask_quiz2_question(message)
    else:
        # Выводим результат викторины
        score = user_data[user_id]["quiz2_score"]
        await message.answer(f"Викторина завершена! Вы ответили верно на {score} из {len(quiz2_questions)} вопросов.", reply_markup=keyboard)
        del user_data[user_id]

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
