import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telethon import TelegramClient

# Bot Tokenini buraya ekleyin
TOKEN = '7024230778:AAGTFI1s7RXz2LNro55NJIO6NVcKSZMwmR8'

# Telethon API ID ve Hash
api_id = '28603118'
api_hash = '35a400855835510c0a926f1e965aa12d'
session_string = 'AgG0cu4AkaIhaB1uFYRvyzOsg-5vaJ7KVPZ-0wghtchiDQDMyjKB6LJdGukLXukl4SR_gr95l-037v6ST0F1vVf458uUUPq_CBOkyk9a8Bb8I39W2Hi1gbDKqVId3NxmnFgsSbLPj1xQtZ5HsDzDXcUVtpfMFiC858P4vc97uFyQd8KpYmjXyMN2XpgT7kI4DA-mVDbegJUVMTwSgue37mdHUF2W_tnFuW4cLQxLT18CQH9UVjpKDzCQi9GBakGDPvm1zVtyWBVj9RcDIfSXu18B1n9V-qV_zxEb0LjtswKCEQPCJWvTTjpGEcyX5z-Q5NQUJGLNt5PQwsBJl03D4WdfFwXsWQAAAAFOeNglAA'

# Telethon istemcisi oluşturuluyor
client = TelegramClient('anon', api_id, api_hash)

# Session string istifadə edilərək müştəri girişini başlatmaq
client = client.start(session=session_string)

# Telegram botu oluşturuluyor
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: CallbackContext):
    welcome_message = "Merhaba! Benimle iletişime geçmek için `/send` komutunu kullanabilirsiniz."
    await update.message.reply_text(welcome_message)

async def send_to_users(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text('Mesaj sağlamalısınız.')
        return

    message = ' '.join(context.args)  # Komuttan sonra gelen tüm mesajı al
    chat_id = update.message.chat_id

    try:
        # Grup yöneticilerini al
        members = await context.bot.get_chat_administrators(chat_id)
        user_ids = [member.user.id for member in members if member.user.id != context.bot.id]

        for user_id in user_ids:
            # Telethon kullanarak gerçek Telegram hesabından mesaj gönderme
            await client.send_message(user_id, message)
            time.sleep(2)  # Spam olmaması için 2 saniye bekleme süresi
    except Exception as e:
        await update.message.reply_text(f'Hata: {str(e)}')

# Komutları ekle
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('send', send_to_users))

# Başlama logu
print("Bot və Telethon istemcisi başlatıldı.")

# Bot ve Telethon istemcisini aynı anda çalıştır
async def main():
    await app.initialize()
    await app.start()
    await client.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
