from turtle import update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

load_dotenv()
TOKEN = os.getenv('8148747209:AAEgNrL6XeuNYEr-AviOyyuPnACjg-Pfy9Q')

async def start(update: update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем кнопку с Web App
    keyboard = [
        [InlineKeyboardButton(
            "🍕 Открыть меню заказа", 
            web_app=WebAppInfo(url="https://your-website.com/telegram-app.html")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Добро пожаловать в сервис заказа еды! 🍔\n\n"
        "Нажмите кнопку ниже чтобы открыть меню:",
        reply_markup=reply_markup
    )

async def handle_web_app_data(update: update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем данные из Web App
    web_app_data = update.message.web_app_data
    data = web_app_data.data  # JSON строка с данными из приложения
    
    import json
    order_data = json.loads(data)
    
    # Обрабатываем заказ
    await update.message.reply_text(
        f"✅ Заказ принят!\n"
        f"Блюдо: {order_data['item']}\n"
        f"Количество: {order_data['quantity']}\n"
        f"Сумма: {order_data['total']} руб."
    )

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    application.run_polling()

if __name__ == '__main__':
    main()