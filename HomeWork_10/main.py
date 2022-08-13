import logging
from pytube import YouTube
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater,
CommandHandler,
MessageHandler,
Filters,
ConversationHandler,
)

#https://www.youtube.com/watch?v=jvipPYFebWc     моё любимое видео


# Включим ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
LINK_COMMAND, PATH_COMMAND, SAVE_COMMAND = range(3)

# функция обратного вызова точки входа в разговор
def start(update, _):
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Привет! Меня зовут YouTube save video bot. Я помогу тебе скачать любое видео с YouTube. '
        'Для этого ты должен ввести ссылку на видео. Командой /cancel можешь прекратить разговор.\n\n'
        'Введи ссылку на видео')
    return LINK_COMMAND

# Обрабатываем сообщение с указанием ссылки на видео
def link_command(update, _):
    global link
    user = update.message.from_user
    logger.info("Пользователь %s указал ссылку на видео: %s", user.first_name, update.message.text)
    update.message.reply_text('Спасибо! Теперь укажи место сохранения.')
    link = update.message.text
    return PATH_COMMAND

# Обрабатываем сообщение с указанием места сохранения
def path_command(update, _):
    global path
    global res
    user = update.message.from_user
    logger.info("Пользователь %s указал место сохранения: %s", user.first_name, update.message.text)
    path = update.message.text
    # Список кнопок для ответа    
    reply_keyboard = [['360p', '720p', '1080p']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Спасибо! Теперь выбери разрешение видео.',
    reply_markup=markup_key)
    res=markup_key
    return SAVE_COMMAND

# Обрабатываем сообщение с указанием разрешения видео
def save_command(update, _):
    update.message.reply_text(
        'Я скачал видео в нужном разрешении. '
        'Можешь наслаждаться просмотром. '
        'Вот некоторые данные о видео. '
        'Для завершения разговора нажми /cancel')
    myVideoStream = YouTube(link)
    update.message.reply_text(f'Название: {myVideoStream.title}')
    update.message.reply_text(f'Продолжительность: {str(myVideoStream.length)} сек')
    update.message.reply_text(f'Количество просмотров: {str(myVideoStream.views)}')
    yt = myVideoStream.streams.filter(file_extension = "mp4", resolution = res)
    yt.first().download(path)
    return ConversationHandler.END

# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Разговор завершен. '
        'Будет скучно - пиши.')
    # Заканчиваем разговор.
    return ConversationHandler.END

if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("5420238978:AAGeUHfhWXxJ4Q4GKyBlmdjvNhj5H-6GvkA")
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями LINE, PATH и RESOLUTION
    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            LINK_COMMAND: [MessageHandler(Filters.text & ~Filters.command, link_command)],
            PATH_COMMAND: [MessageHandler(Filters.text & ~Filters.command, path_command)],
            SAVE_COMMAND: [MessageHandler(Filters.regex('^(360p|720p|1080p)$'), save_command)]},
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()