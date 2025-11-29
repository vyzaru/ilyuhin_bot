import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# URL будет устанавливаться динамически через ngrok
WEB_APP_URL = "https://your-ngrok-url.ngrok.io"  # Замените на ваш ngrok URL

# Основная клавиатура с Web App кнопкой
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Открыть приложение", web_app=WebAppInfo(url=WEB_APP_URL))],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="👋 Привет")]
    ],
    resize_keyboard=True
)

# Inline клавиатура с Web App
def get_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Запустить приложение", web_app=WebAppInfo(url=WEB_APP_URL))
    builder.button(text="📊 Статистика", callback_data="stats")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Нажмите кнопку ниже, чтобы открыть мини-приложение:",
        reply_markup=main_keyboard
    )
    
    # Также отправляем inline клавиатуру
    await message.answer(
        "Или используйте inline кнопку:",
        reply_markup=get_inline_keyboard()
    )

@dp.message(Command("app"))
async def cmd_app(message: Message):
    await message.answer(
        "📱 Запуск мини-приложения:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Открыть приложение", web_app=WebAppInfo(url=WEB_APP_URL))]],
            resize_keyboard=True
        )
    )

# Обработчик данных из Web App
@dp.message(F.content_type == "web_app_data")
async def handle_web_app_data(message: Message):
    data = message.web_app_data.data
    button_text = message.web_app_data.button_text
    
    await message.answer(
        f"📨 Данные из приложения:\n"
        f"Кнопка: {button_text}\n"
        f"Данные: {data}"
    )

@dp.callback_query(F.data == "stats")
async def handle_stats_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("📊 Статистика: 100 пользователей")

@dp.message(F.text == "📱 Открыть приложение")
async def open_web_app(message: Message):
    await message.answer(
        "Нажмите на кнопку ниже для открытия приложения:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Открыть приложение", web_app=WebAppInfo(url=WEB_APP_URL))]],
            resize_keyboard=True
        )
    )

# Остальные обработчики...
@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
📋 Доступные команды:

/start - Начать работу
/app - Открыть мини-приложение
/help - Помощь

🎛 Кнопки:
📱 Открыть приложение - Запуск веб-приложения
👋 Привет - Поздороваться
    """
    await message.answer(help_text)

async def main():
    print("Бот с Web App запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())