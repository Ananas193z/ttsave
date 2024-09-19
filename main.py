import logging
import re
import os
import pickle
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Токен вашего бота
API_TOKEN = '8052252656:AAFniHx8WCtCsC_k3F-SPKtWsw6KoWd_5f4'

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Список каналов для подписки
channels = [
    'https://t.me/ggagahahajjx',
    'https://t.me/nqjajanannana',
    'https://t.me/akqlqlqlpqpq'
]
special_users_for_bot = {
    1651997919
}

# Загрузка списка пользователей
try:
    with open("users.pkl", "rb") as file:
        users_category = pickle.load(file)
except FileNotFoundError:
    users_category = []

# Функция для добавления пользователя в список
def add_user(user_point):
    if user_point not in users_category:
        users_category.append(user_point)
        print(f"Пользователь '{user_point}' успешно добавлен.")
        save_users_file()
    else:
        print(f"Пользователь '{user_point}' уже в списке.")

# Функция для сохранения данных в файл
def save_users_file():
    with open("users.pkl", "wb") as file:
        pickle.dump(users_category, file)



for i in special_users_for_bot:
    if i in users_category:
        pass
    else:
        add_user(i)




# Загрузка списка пользователей
try:
    with open("polzovateliwas.pkl", "rb") as file:
        polzovateliwas_category = pickle.load(file)
except FileNotFoundError:
    polzovateliwas_category = []

# Функция для добавления пользователя в список
def add_polzovateliwas(polzovateliwas_point):
    if polzovateliwas_point not in polzovateliwas_category:
        polzovateliwas_category.append(polzovateliwas_point)
        print(f"Пользователь '{polzovateliwas_point}' успешно добавлен.")
        save_polzovateliwas_file()
    else:
        print(f"Пользователь '{polzovateliwas_point}' уже в списке.")
# Функция для сохранения данных в файл
def save_polzovateliwas_file():
    with open("polzovateliwas.pkl", "wb") as file:
        pickle.dump(polzovateliwas_category, file)














# Функция для загрузки видео из TikTok
def download_tiktok_video(video_url, save_path='tiktok_videos'):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        logging.error(f"Ошибка при скачивании видео: {str(e)}")
        return None












# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    if user_id in polzovateliwas_category:
        pass
    else:
        add_polzovateliwas(user_id)

    if user_id in users_category:
        await message.reply("Привет! Отправь мне ссылку на видео из 🔗TikTok🔗, и я скачаю его без водяного знака.⬇️")
    else:
        markup = InlineKeyboardMarkup()
        for i in channels:
            match = re.search(r'https://t\.me/([A-Za-z0-9_]+)', i)
            if match:
                channel_username = match.group(1)
                subscribe_button = InlineKeyboardButton(channel_username, url=i)
                markup.add(subscribe_button)
        done_button = InlineKeyboardButton("Готово", callback_data="subscription_check_but_pressed")
        markup.add(done_button)
        await message.reply("Привет! Подпишитесь на каналы, чтобы продолжить.", reply_markup=markup)





# Обработчик для кнопки "Готово"
@dp.callback_query_handler(lambda c: c.data == 'subscription_check_but_pressed')
async def check_subs(callback: CallbackQuery):
    user_id = callback.from_user.id
    not_subscribed_channels = []

    for i in channels:
        match = re.search(r'https://t\.me/([A-Za-z0-9_]+)', i)
        if match:
            channel_username = match.group(1)
            try:
                user_channel_status = await bot.get_chat_member(chat_id=f'@{channel_username}', user_id=user_id)
                logging.info(f"User ID: {user_id} - Status in channel @{channel_username}: {user_channel_status.status}")

                if user_channel_status.status == 'left':
                    not_subscribed_channels.append(channel_username)
            except Exception as e:
                logging.error(f"Ошибка при проверке подписки: {e}")
                await callback.answer('Не удалось проверить подписку. Попробуйте снова.')
                return

    if not_subscribed_channels:
        if len(not_subscribed_channels) == len(channels):
            await callback.answer('Вы не подписаны ни на один из каналов. Пожалуйста, подпишитесь на все каналы.')
        else:
            await callback.answer(f'Вы подписаны не на все каналы. Необходимо подписаться на следующие каналы: {", ".join(not_subscribed_channels)}.')
    else:
        add_user(user_id)
        await callback.answer('Спасибо за подписку на все каналы! ✅')
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.send_message(callback.message.chat.id, 'Привет! Отправь мне ссылку на видео из 🔗TikTok🔗 , и я скачаю его без водяного знака.⬇️')













# Обработчик текстовых сообщений (ссылок на видео)
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_video_download(message: types.Message):
    user_id = message.from_user.id

    if user_id in users_category:
        url = message.text.strip()
        if "tiktok.com" not in url:
            await message.reply("🔗Это не похоже на ссылку TikTok🔗\nПопробуй снова.🔄")
            return

        try:
            print(f"Получена ссылка: {url}")
            await bot.send_message(message.chat.id, '🔄Скачиваю...🔄')
            filename = download_tiktok_video(url)
            
            if filename:
                print(f"Видео успешно скачано: {filename}")
                with open(filename, "rb") as video_file:
                    await bot.send_video(message.chat.id, video=video_file, caption="Вот ваше видео без водяного знака! ✅")
                print("Видео отправлено пользователю")
                os.remove(filename)
                print(f"Файл {filename} удалён.")
            else:
                await message.reply("Не удалось скачать видео. Попробуйте снова.")
        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")
            await message.reply("Произошла ошибка при обработке запроса.")
    else:
        await message.reply("Вы не подписаны на каналы, подпишитесь пожалуйста.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
