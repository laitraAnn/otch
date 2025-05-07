from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "7136972649:AAFIZLo1ZFPzOit2-YiEbWpm4kn5Ec3mdoA"
# ID канала (например, @testchannel → передавайте как "-1001234567890")
CHANNEL_ID = "-1001522061930"  

def start(update: Update, context: CallbackContext) -> None:
    """Команда /start для проверки бота"""
    update.message.reply_text("Бот работает! Используйте /post для создания поста в канале.")

def create_post(update: Update, context: CallbackContext) -> None:
    """Создаёт пост в канале с кнопкой"""
    keyboard = [[InlineKeyboardButton("Нажми меня!", callback_data="user_click")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="Это пост с кнопкой. Нажмите на неё, чтобы бот записал ваш username!",
        reply_markup=reply_markup
    )
    update.message.reply_text("Пост опубликован в канале!")

def button_click(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатие на кнопку"""
    query = update.callback_query
    user = query.from_user
    username = user.username  # Получаем username пользователя
    
    if username:
        # Отправляем сообщение в ЛС пользователю
        context.bot.send_message(
            chat_id=user.id,
            text=f"Ваш username (@{username}) был записан!"
        )
        
        # Логируем в консоль (можно сохранять в базу данных)
        logger.info(f"Пользователь @{username} нажал на кнопку.")
        
        # Подтверждаем нажатие (убираем "часики" на кнопке)
        query.answer(f"Спасибо, @{username}! Ваш username записан.")
    else:
        query.answer("У вас нет username в Telegram!")

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("post", create_post))
    dp.add_handler(CallbackQueryHandler(button_click, pattern="^user_click$"))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()