import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telethon import TelegramClient

# Bot Tokenini buraya ekleyin
TOKEN = '7024230778:AAGTFI1s7RXz2LNro55NJIO6NVcKSZMwmR8'

# Telethon API ID və Hash
api_id = '28603118'
api_hash = '35a400855835510c0a926f1e965aa12d'
session_string = 'my_session'  # Basit bir dosya adı

# Telethon müştərisini başlatmaq
client = TelegramClient(session_string, api_id, api_hash)

# Telegram botu yaradılır
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Merhaba! Benimle iletişime geçmek için `/send` komutunu kullanabilirsiniz."
    await update.message.reply_text(welcome_message)

async def send_to_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update.message.text.split()) < 2:
        await update.message.reply_text('Mesaj sağlamalısınız.')
        return

    message = ' '.join(update.message.text.split()[1:])
    chat_id = update.message.chat_id

    try:
        # Qrup rəhbərlərini al
        members = await context.bot.get_chat_administrators(chat_id)
        user_ids = [member.user.id for member in members if member.user.id != context.bot.id]

        for user_id in user_ids:
            # Telethon istifadə edərək real Telegram hesabından mesaj göndər
            await client.send_message(user_id, message)
            await asyncio.sleep(2)  # Spam olmaması üçün 2 saniyə gözləmə müddəti
    except Exception as e:
        await update.message.reply_text(f'Hata: {str(e)}')

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('send', send_to_users))

print("Bot və Telethon müştərisi işə salındı.")

async def main():
    # Telethon müştərisini başlat
    await client.start()
    await app.initialize()
    await app.start()
    await app.run_polling()
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
