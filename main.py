import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import ReplyKeyboardMarkup
import matplotlib.pyplot as plt
from io import BytesIO
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler




# Получение курса BTC с CoinDesk
print("=== 🚀 Стартую актуальный main.py ===")

#def get_btc_price():
#    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
#    print(f"👀 Делаю запрос к: {url}")

#    try:
#        response = requests.get(url)
#        data = response.json()
#        price = data["bitcoin"]["usd"]
#        return f"💸 Курс биткоина: ${price}"
#    except Exception as e:
#        return f"Ошибка при получении курса: {str(e)}"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,eur,uah,rub"
    print(f"👀 Делаю запрос к: {url}")

    try:
        response = requests.get(url)
        data = response.json()
        btc = data["bitcoin"]
        return (
            f"💸 Курс Биткоина:\n"
            f"🇺🇸 USD: ${btc['usd']}\n"
            f"🇪🇺 EUR: €{btc['eur']}\n"
            f"🇺🇦 UAH: ₴{btc['uah']}\n"
            f"🇷🇺 RUB: ₽{btc['rub']}"
        )
    except Exception as e:
        return f"Ошибка при получении курса BTC: {str(e)}"

def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd,eur,uah,rub"
    print(f"👀 Делаю запрос к: {url}")

    try:
        response = requests.get(url)
        data = response.json()
        eth = data["ethereum"]
        return (
            f"💸 Курс Ethereum:\n"
            f"🇺🇸 USD: ${eth['usd']}\n"
            f"🇪🇺 EUR: €{eth['eur']}\n"
            f"🇺🇦 UAH: ₴{eth['uah']}\n"
            f"🇷🇺 RUB: ₽{eth['rub']}"
        )
    except Exception as e:
        return f"Ошибка при получении курса ETH: {str(e)}"

async def btc_chart(chat_id, bot):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"
    print(f"📊 Запрашиваю график для chat_id: {chat_id}")

    try:
        response = requests.get(url)
        data = response.json()
        prices = data["prices"]

        times = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
        values = [p[1] for p in prices]

        plt.figure(figsize=(8, 4))
        plt.plot(times, values)
        plt.title("Курс BTC за 24ч")
        plt.xlabel("Время")
        plt.ylabel("USD")
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        await bot.send_photo(chat_id=chat_id, photo=buf)

    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"Ошибка при получении графика: {str(e)}")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /start от", update.effective_user.username)

    keyboard = [
        [InlineKeyboardButton("📈 Курс BTC", callback_data="btc_price")],
        [InlineKeyboardButton("📉 Курс ETH", callback_data="eth_price")],
        [InlineKeyboardButton("📊 График BTC", callback_data="btc_chart")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выберите действие 👇",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat.id
    print(f"Нажата кнопка: {data}")

    if data == "btc_price":
        price = get_btc_price()
        await query.message.reply_text(price)

    elif data == "eth_price":
        price = get_eth_price()
        await query.message.reply_text(price)

    elif data == "btc_chart":
        await btc_chart(chat_id, context.bot)



# Команда /start с кнопками
#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    print("Получена команда /start от", update.effective_user.username)

#    keyboard = [["/btc", "/eth", "/chart"]]
#    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

#    await update.message.reply_text(
#        "Привет! Выбери валюту, чтобы узнать курс 👇",
#        reply_markup=markup
#    )

# Команда /btc
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /btc от", update.effective_user.username)
    price = get_btc_price()
    await update.message.reply_text(price)

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /eth от", update.effective_user.username)
    price = get_eth_price()
    await update.message.reply_text(price)



# Точка входа
if __name__ == '__main__':
    app = ApplicationBuilder().token("7264724437:AAEtjwkOax_uburdBeftJcWrVoIhxG_Y4hk").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("eth", eth))
    app.add_handler(CommandHandler("chart", btc_chart))
    app.add_handler(CallbackQueryHandler(handle_buttons))



    print("✅ Бот запущен. Нажимай Ctrl+C для остановки.")
    app.run_polling()
