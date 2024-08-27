import time
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Bot Tokenini buraya ekle
TOKEN = '7024230778:AAGTFI1s7RXz2LNro55NJIO6NVcKSZMwmR8'

# Kullanıcı botunun oturumunu temsil eden sınıf
class UserBot:
    def __init__(self, session_id):
        self.session_id = session_id

    def send_message(self, user_id, message):
        # Burada kullanıcı hesabını kullanarak mesaj gönderme kodunu ekle
        print(f"UserBot {self.session_id} gönderiyor: {message} -> {user_id}")

# Kullanıcı botunun oturumunu oluştur
user_bot = UserBot('SESSION_ID_1')

# Botunuzu oluşturun
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: CallbackContext):
    welcome_message = "Merhaba! Benimle iletişime geçmek için `/send` komutunu kullanabilirsiniz."
    await update.message.reply_text(welcome_message)

async def send_to_users(update: Update, context: CallbackContext):
    message = ' '.join(context.args[1:])  # Komuttan sonra gelen mesajı al
    if not message:
        await update.message.reply_text('Mesaj sağlamalısınız.')
        return

    chat_id = update.message.chat_id

    try:
        members = await context.bot.get_chat_administrators(chat_id)
        user_ids = [member.user.id for member in members if member.user.id != context.bot.id]

        for user_id in user_ids:
            user_bot.send_message(user_id, message)  # Kullanıcı botu ile mesaj gönder
            time.sleep(2)  # Spam olmaması için 2 saniye bekleme süresi
    except Exception as e:
        await update.message.reply_text(f'Hata: {str(e)}')

# Komutları ekle
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('send', send_to_users))

# Başlama logu
print("Bot başlatıldı.")

app.run_polling()
