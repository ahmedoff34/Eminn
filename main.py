import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Bot Tokenini buraya ekle
TOKEN = 'YOUR_BOT_TOKEN'

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
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def send_to_users(update, context):
    message = ' '.join(context.args[1:])  # Komuttan sonra gelen mesajı al
    if not message:
        update.message.reply_text('Mesaj sağlamalısınız.')
        return

    # Burada gruptaki üyeleri alacak ve kullanıcı botuna mesaj gönderecek fonksiyonu çağır
    user_ids = get_group_members(update.message.chat_id)
    
    for user_id in user_ids:
        user_bot.send_message(user_id, message)
        time.sleep(2)  # Spam olmaması için 2 saniye bekleme süresi

def get_group_members(chat_id):
    # Burada gruptaki üyeleri alacak kodu yazmalısın
    return [123456789]  # Örnek kullanıcı ID'si

send_message_handler = CommandHandler('send', send_to_users)
dispatcher.add_handler(send_message_handler)

updater.start_polling()
updater.idle()
