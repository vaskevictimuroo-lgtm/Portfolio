import os
import time
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from collections import defaultdict
import sys
import psutil
import requests
from datetime import datetime, timedelta

load_dotenv()

cold_start = True


def get_bot_token():
    token = os.getenv('BOT_TOKEN')
    if not token:
        token = "7848065335:AAG2Ek4Kh76L4m3NPxN39FsuFm7aFMAz5Zw"

    if not token or token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Bot token not found! Set BOT_TOKEN environment variable")

    return token


BOT_TOKEN = get_bot_token()
bot = telebot.TeleBot(BOT_TOKEN)

moderators_chat_id = -1003005577058
moderators = set()
user_messages = {}
waiting_for_moderators_chat = False

user_message_timestamps = defaultdict(list)
MAX_MESSAGES_PER_MINUTE = 20

OWNER_ID = 5492264667


def keep_alive_ping():
    ping_urls = [
        'https://test-plqd.onrender.com/health',
        'https://test-plqd.onrender.com/'
    ]

    while True:
        success = False
        for url in ping_urls:
            try:
                response = requests.get(url, timeout=30)
                print(f"✅ Keep-alive ping to {url}: {response.status_code}")
                success = True
                break
            except Exception as e:
                print(f"❌ Keep-alive failed for {url}: {e}")

        if not success:
            print("⚠️ All keep-alive attempts failed")

        time.sleep(300)


def start_keep_alive():
    ping_thread = threading.Thread(target=keep_alive_ping, daemon=True)
    ping_thread.start()


def handle_cold_start():
    global cold_start
    if cold_start:
        print("🔥 Cold start - bot was sleeping")
        cold_start = False
        try:
            if OWNER_ID:
                bot.send_message(
                    OWNER_ID,
                    "🤖 Бот проснулся после сна\n"
                    f"⏰ Время: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
        except Exception as e:
            print(f"⚠️ Could not send cold start notification: {e}")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/health' or self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
                print(f"✅ Health check: {self.path}")
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Telegram Bot is running!')
                print(f"✅ Request: {self.path}")

        except Exception as e:
            print(f"❌ HTTP error: {e}")
            self.send_error(500, f"Server error: {e}")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def log_message(self, format, *args):
        print(f"🌐 HTTP: {self.address_string()} - {self.command} {self.path}")


def run_http_server():
    port = 5000
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🌐 HTTP server running on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"❌ HTTP server crashed: {e}")
        time.sleep(5)
        run_http_server()


def check_flood(user_id):
    now = time.time()

    user_message_timestamps[user_id] = [
        t for t in user_message_timestamps[user_id]
        if now - t < 300
    ]

    messages_last_minute = [t for t in user_message_timestamps[user_id] if now - t < 60]
    messages_last_5min = user_message_timestamps[user_id]

    if len(messages_last_minute) >= 5:
        return False
    if len(messages_last_5min) >= 20:
        return False

    user_message_timestamps[user_id].append(now)
    return True


def create_reply_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📨 Ответить", callback_data=f"reply_{user_id}"))
    return keyboard


def refresh_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔄 Обновить модераторов", callback_data="refresh_mods"))
    return keyboard


def update_moderators_from_chat():
    global moderators
    if not moderators_chat_id:
        return False

    try:
        chat_admins = bot.get_chat_administrators(moderators_chat_id)
        moderators.clear()

        moderators.add(OWNER_ID)

        for admin in chat_admins:
            if not admin.user.is_bot:
                moderators.add(admin.user.id)

        print(f"Обновлен список модераторов: {moderators}")
        return True

    except Exception as e:
        print(f"Ошибка при обновлении модераторов: {e}")
        return False


def is_moderator(user_id):
    if user_id == OWNER_ID:
        return True

    return user_id in moderators


def get_user_info(user_id):
    try:
        user = bot.get_chat(user_id)
        info = f"👤 Информация о пользователе:\n"
        info += f"• ID: {user.id}\n"
        info += f"• Имя: {user.first_name}\n"
        if user.last_name:
            info += f"• Фамилия: {user.last_name}\n"
        if user.username:
            info += f"• @username: @{user.username}\n"

        msg_count = len(user_message_timestamps[user_id])
        info += f"• 📊 Сообщений сегодня: {msg_count}\n"

        return info
    except Exception as e:
        return f"❌ Не удалось получить информацию о пользователе: {e}"


@bot.message_handler(commands=['start'])
def start_command(message):
    handle_cold_start()
    if message.from_user.id == OWNER_ID:
        bot.send_message(message.chat.id,
                         "👋 Владелец бота! Используйте команды:\n"
                         "/setup - настроить чат модераторов\n"
                         "/refresh - обновить список модераторов\n"
                         "/stats - статистика бота\n"
                         f"✅ Ваш ID: {message.from_user.id}\n"
                         f"✅ Вы модератор: {is_moderator(message.from_user.id)}")
    elif moderators_chat_id and message.chat.id == moderators_chat_id:
        if update_moderators_from_chat():
            bot.send_message(message.chat.id,
                             f"👋 Добро пожаловать в чат модераторов! Ваши права обновлены.\n"
                             f"✅ Вы модератор: {is_moderator(message.from_user.id)}",
                             reply_markup=refresh_keyboard())
        else:
            bot.send_message(message.chat.id, "👋 Добро пожаловать! Для работы обратитесь к владельцу.")
    else:
        bot.send_message(message.chat.id, "👋 Привет! Отправь мне сообщение, и я передам его модераторам.")


@bot.message_handler(commands=['setup'])
def setup_command(message):
    handle_cold_start()
    if message.from_user.id == OWNER_ID:
        global waiting_for_moderators_chat
        waiting_for_moderators_chat = True
        bot.send_message(message.chat.id,
                         "Добавьте бота в чат модераторов (с правами администратора!) и перешлите любое сообщение из этого чата:")
    else:
        bot.send_message(message.chat.id, "❌ Эта команда доступна только владельцу.")


@bot.message_handler(commands=['refresh'])
def refresh_command(message):
    handle_cold_start()
    if is_moderator(message.from_user.id):
        if update_moderators_from_chat():
            bot.send_message(message.chat.id,
                             f"✅ Список модераторов обновлен! Всего модераторов: {len(moderators)}\n"
                             f"👑 Владелец: {OWNER_ID}\n"
                             f"✅ Вы модератор: {is_moderator(message.from_user.id)}",
                             reply_markup=refresh_keyboard())
        else:
            bot.send_message(message.chat.id, "❌ Ошибка при обновлении модераторов. Проверьте настройки чата.")
    else:
        bot.send_message(message.chat.id,
                         f"❌ Эта команда доступна только модераторам.\n"
                         f"Ваш ID: {message.from_user.id}")


@bot.message_handler(commands=['stats'])
def stats_command(message):
    handle_cold_start()
    if message.from_user.id == OWNER_ID:
        stats_text = f"📊 Статистика бота:\n"
        stats_text += f"• Чат модераторов: {moderators_chat_id or 'Не настроен'}\n"
        stats_text += f"• Модераторов: {len(moderators)}\n"
        stats_text += f"• Владелец: {OWNER_ID}\n"
        stats_text += f"• Активных пользователей: {len(user_message_timestamps)}\n"
        stats_text += f"• Сообщений в памяти: {len(user_messages)}"
        bot.send_message(message.chat.id, stats_text)
    else:
        bot.send_message(message.chat.id, "❌ Эта команда доступна только владельцу.")


@bot.message_handler(commands=['status'])
def status_command(message):
    handle_cold_start()

    status_text = (
        f"🤖 Статус бота:\n"
        f"• 📊 Пользователей сегодня: {len(user_message_timestamps)}\n"
        f"• 👮 Модераторов: {len(moderators)}\n"
        f"• 👑 Владелец: {OWNER_ID}\n"
        f"• 🕒 Время работы: {time.strftime('%H:%M:%S')}\n"
        f"• ❄️ Холодный старт: {'Да' if cold_start else 'Нет'}\n"
        f"• ✅ Вы модератор: {is_moderator(message.from_user.id)}"
    )

    bot.send_message(message.chat.id, status_text)


@bot.message_handler(commands=['info'])
def info_command(message):
    handle_cold_start()
    if not is_moderator(message.from_user.id):
        bot.send_message(message.chat.id,
                         f"❌ Эта команда доступна только модераторам.\n"
                         f"Ваш ID: {message.from_user.id}")
        return

    if message.reply_to_message:
        reply_to_msg_id = message.reply_to_message.message_id
        if reply_to_msg_id in user_messages:
            user_id = user_messages[reply_to_msg_id]
            info = get_user_info(user_id)
            bot.send_message(message.chat.id, info)
        else:
            bot.send_message(message.chat.id, "❌ Это не сообщение от пользователя.")
    else:
        bot.send_message(message.chat.id, "❌ Ответьте на сообщение пользователя чтобы получить информацию.")


@bot.message_handler(commands=['debug'])
def debug_command(message):
    handle_cold_start()
    if message.from_user.id == OWNER_ID:
        debug_text = f"🔧 Отладочная информация:\n"
        debug_text += f"• Ваш ID: {message.from_user.id}\n"
        debug_text += f"• Владелец: {OWNER_ID}\n"
        debug_text += f"• Вы владелец: {message.from_user.id == OWNER_ID}\n"
        debug_text += f"• Вы модератор: {is_moderator(message.from_user.id)}\n"
        debug_text += f"• Чат модераторов: {moderators_chat_id}\n"
        debug_text += f"• Список модераторов: {moderators}\n"
        debug_text += f"• Всего модераторов: {len(moderators)}"
        bot.send_message(message.chat.id, debug_text)
    else:
        bot.send_message(message.chat.id, "❌ Эта команда доступна только владельцу.")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    handle_cold_start()
    global waiting_for_moderators_chat

    if message.text.startswith('/'):
        return

    if waiting_for_moderators_chat:
        setup_moderators_chat(message)
        return

    if moderators_chat_id and message.chat.id == moderators_chat_id:
        handle_moderator_chat_message(message)
    elif message.from_user.id == OWNER_ID and message.chat.type == 'private':
        handle_owner_message(message)
    else:
        if not check_flood(message.from_user.id):
            bot.send_message(message.chat.id, "❌ Слишком много сообщений! Подождите немного.")
            return

        forward_to_moderators_chat(message)


@bot.message_handler(content_types=['photo', 'document', 'video', 'audio', 'voice', 'sticker'])
def handle_media(message):
    handle_cold_start()

    if moderators_chat_id and message.chat.id == moderators_chat_id:
        handle_moderator_chat_message(message)
    else:
        if not check_flood(message.from_user.id):
            bot.send_message(message.chat.id, "❌ Слишком много сообщений! Подождите немного.")
            return

        forward_to_moderators_chat(message)


def setup_moderators_chat(message):
    global moderators_chat_id, waiting_for_moderators_chat

    if message.forward_from_chat:
        moderators_chat_id = message.forward_from_chat.id
        waiting_for_moderators_chat = False

        if update_moderators_from_chat():
            bot.send_message(message.chat.id,
                             f"✅ Чат модераторов установлен! ID: {moderators_chat_id}\nМодераторов: {len(moderators)}")
            bot.send_message(moderators_chat_id,
                             "✅ Этот чат теперь является чатом модераторов! Все администраторы чата могут отвечать на сообщения пользователей.",
                             reply_markup=refresh_keyboard())
        else:
            bot.send_message(message.chat.id,
                             "❌ Не удалось получить список администраторов. Убедитесь, что бот имеет права администратора в чате.")

    elif message.chat.type in ['group', 'supergroup']:
        moderators_chat_id = message.chat.id
        waiting_for_moderators_chat = False

        if update_moderators_from_chat():
            bot.send_message(message.chat.id,
                             f"✅ Этот чат установлен как чат модераторов! ID: {moderators_chat_id}\nМодераторов: {len(moderators)}",
                             reply_markup=refresh_keyboard())
        else:
            bot.send_message(message.chat.id,
                             "❌ Не удалось получить список администраторов. Убедитесь, что бот имеет права администратора в чате.")

    else:
        bot.send_message(message.chat.id,
                         "❌ Пожалуйста, перешлите сообщение из группового чата или выполните команду в нужном чате.")


def forward_to_moderators_chat(message):
    if not moderators_chat_id:
        bot.send_message(message.chat.id, "❌ Чат модераторов еще не настроен. Попробуйте позже.")
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if message.from_user.username:
        user_name += f" (@{message.from_user.username})"

    try:
        if message.content_type == 'text':
            sent_message = bot.send_message(
                moderators_chat_id,
                f"👤 Сообщение от {user_name} (ID: {user_id}):\n\n{message.text}",
                reply_markup=create_reply_keyboard(user_id)
            )
        else:
            caption = f"👤 Сообщение от {user_name} (ID: {user_id})"
            if message.caption:
                caption += f":\n\n{message.caption}"

            if message.content_type == 'photo':
                sent_message = bot.send_photo(
                    moderators_chat_id,
                    message.photo[-1].file_id,
                    caption=caption,
                    reply_markup=create_reply_keyboard(user_id)
                )
            elif message.content_type == 'document':
                sent_message = bot.send_document(
                    moderators_chat_id,
                    message.document.file_id,
                    caption=caption,
                    reply_markup=create_reply_keyboard(user_id)
                )
            elif message.content_type == 'video':
                sent_message = bot.send_video(
                    moderators_chat_id,
                    message.video.file_id,
                    caption=caption,
                    reply_markup=create_reply_keyboard(user_id)
                )
            elif message.content_type == 'audio':
                sent_message = bot.send_audio(
                    moderators_chat_id,
                    message.audio.file_id,
                    caption=caption,
                    reply_markup=create_reply_keyboard(user_id)
                )
            elif message.content_type == 'voice':
                sent_message = bot.send_voice(
                    moderators_chat_id,
                    message.voice.file_id,
                    caption=caption,
                    reply_markup=create_reply_keyboard(user_id)
                )
            elif message.content_type == 'sticker':
                sent_message = bot.send_sticker(
                    moderators_chat_id,
                    message.sticker.file_id
                )
                bot.send_message(
                    moderators_chat_id,
                    f"👤 Стикер от {user_name} (ID: {user_id})",
                    reply_markup=create_reply_keyboard(user_id)
                )

        user_messages[sent_message.message_id] = user_id
        print(f"✅ Сообщение {sent_message.message_id} сохранено для пользователя {user_id}")

        bot.send_message(message.chat.id, "✅ Ваше сообщение отправлено модераторам!")

    except Exception as e:
        print(f"Ошибка при отправке в чат модераторов: {e}")
        bot.send_message(message.chat.id, "❌ Ошибка при отправке сообщения. Попробуйте позже.")


def handle_moderator_chat_message(message):
    if message.text and message.text.startswith('/'):
        return

    if not is_moderator(message.from_user.id):
        bot.send_message(message.chat.id,
                         f"❌ Вы не являетесь модератором. Для получения прав обратитесь к владельцу чата.\n"
                         f"Ваш ID: {message.from_user.id}\n"
                         f"Владелец: {OWNER_ID}")
        return

    if message.reply_to_message:
        reply_to_msg_id = message.reply_to_message.message_id
        print(f"🔍 Поиск сообщения {reply_to_msg_id} в базе: {list(user_messages.keys())[:5]}...")

        if reply_to_msg_id in user_messages:
            user_id = user_messages[reply_to_msg_id]
            print(f"✅ Найден пользователь {user_id} для сообщения {reply_to_msg_id}")

            try:
                moderator_name = message.from_user.first_name
                if message.from_user.username:
                    moderator_name += f" (@{message.from_user.username})"

                if message.content_type == 'text':
                    bot.send_message(user_id,
                                     f"📩 Ответ от модератора {moderator_name}:\n\n{message.text}")
                else:
                    caption = f"📩 Ответ от модератора {moderator_name}"
                    if message.caption:
                        caption += f":\n\n{message.caption}"

                    if message.content_type == 'photo':
                        bot.send_photo(user_id, message.photo[-1].file_id, caption=caption)
                    elif message.content_type == 'document':
                        bot.send_document(user_id, message.document.file_id, caption=caption)
                    elif message.content_type == 'video':
                        bot.send_video(user_id, message.video.file_id, caption=caption)
                    elif message.content_type == 'audio':
                        bot.send_audio(user_id, message.audio.file_id, caption=caption)
                    elif message.content_type == 'voice':
                        bot.send_voice(user_id, message.voice.file_id, caption=caption)
                    elif message.content_type == 'sticker':
                        bot.send_sticker(user_id, message.sticker.file_id)
                        bot.send_message(user_id, f"📩 Стикер от модератора {moderator_name}")

                bot.send_message(moderators_chat_id,
                                 f"✅ Ответ отправлен пользователю {user_id}!")

            except Exception as e:
                error_msg = f"❌ Не удалось отправить ответ: {e}"
                print(error_msg)
                bot.send_message(moderators_chat_id, error_msg)
        else:
            print(f"❌ Сообщение {reply_to_msg_id} не найдено в базе")
            bot.send_message(moderators_chat_id,
                             "❌ Это не сообщение от пользователя или оно устарело.")


def handle_owner_message(message):
    if message.text == "Обновить модераторов":
        if update_moderators_from_chat():
            bot.send_message(message.chat.id, f"✅ Список модераторов обновлен! Всего: {len(moderators)}")
        else:
            bot.send_message(message.chat.id, "❌ Ошибка при обновлении. Проверьте права бота в чате.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        print(f"🔔 Callback received: {call.data} from {call.from_user.id}")

        if call.data.startswith('reply_'):
            user_id = int(call.data.split('_')[1])
            bot.answer_callback_query(call.id,
                                      "📨 Ответьте (reply) на это сообщение чтобы отправить ответ пользователю")

        elif call.data.startswith('info_'):
            user_id = int(call.data.split('_')[1])
            info = get_user_info(user_id)
            bot.answer_callback_query(call.id, "📊 Информация о пользователе")
            bot.send_message(call.message.chat.id, info)

        elif call.data == "refresh_mods":
            if is_moderator(call.from_user.id):
                if update_moderators_from_chat():
                    bot.answer_callback_query(call.id, "✅ Список модераторов обновлен!")
                    bot.edit_message_text(f"✅ Список модераторов обновлен! Всего: {len(moderators)}",
                                          call.message.chat.id, call.message.message_id,
                                          reply_markup=refresh_keyboard())
                else:
                    bot.answer_callback_query(call.id, "❌ Ошибка при обновлении")
            else:
                bot.answer_callback_query(call.id, "❌ Только для модераторов")

    except Exception as e:
        print(f"❌ Ошибка в callback: {e}")
        bot.answer_callback_query(call.id, "❌ Ошибка обработки")


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_members(message):
    handle_cold_start()
    if message.chat.id == moderators_chat_id:
        for new_member in message.new_chat_members:
            if not new_member.is_bot:
                bot.send_message(moderators_chat_id,
                                 f"👋 Добро пожаловать, {new_member.first_name}! Для получения прав модератора обратитесь к владельцу.")


def run_bot_with_restart():
    restart_attempts = 0
    max_restarts = 5

    while restart_attempts < max_restarts:
        try:
            print("🤖 Starting Telegram bot...")
            bot.infinity_polling(
                allowed_updates=['message', 'callback_query'],
                timeout=90,
                long_polling_timeout=90,
                skip_pending=True
            )
        except Exception as e:
            restart_attempts += 1
            print(f"❌ Bot crashed (attempt {restart_attempts}/{max_restarts}): {e}")

            if restart_attempts >= max_restarts:
                print("🚨 Max restart attempts reached. Exiting.")
                break

            wait_time = min(30 * restart_attempts, 300)
            print(f"🔄 Restarting in {wait_time} seconds...")
            time.sleep(wait_time)


def main():
    print("🚀 Initializing Telegram Moderator Bot...")

    try:
        import psutil
        import requests
        import telebot
        from dotenv import load_dotenv
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install with: pip install -r requirements.txt")
        return

    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    print("🌐 HTTP server started on port 5000")

    start_keep_alive()
    print("🔄 Keep-alive service started")

    try:
        if moderators_chat_id:
            update_moderators_from_chat()

        print(f"✅ Владелец бота: {OWNER_ID}")
        print(f"✅ Модераторов в списке: {len(moderators)}")

        run_bot_with_restart()

    except KeyboardInterrupt:
        print("👋 Bot stopped by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()