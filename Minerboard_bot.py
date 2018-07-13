# build by OZOAR 29/06/2018
# almost for fun

from sqlite import DataBase
import telebot
import config
import time
import re

admin_id = 391058952
admin_chat = -242521427

idinahoi_list = ['дурак', 'жопа']

help_info = "This is official Minerboard Support Bot.\nHere you can ask any question and get feedback.\nVisit our web-site."
greeting_info = 'Welcome to  Minerboard Support Bot avalible commands:\n/help - info about project\n/start - info about bot' \
                '\nAlso MinerBoard Bot can also grab your last one photo and receive it to our technical specialists'
faq_message = 'You can find Minerboard FAQ here:'
greeting_words = ['hi', 'hello', 'хай', 'привет', 'ghbdtn', 'рш']

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda message: message.text != None and message.text.lower() in greeting_words)
def command_text_hi(message):
    bot.send_message(message.chat.id, "Hi! What`s problem dude ?\nYou can ask any question.")
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])


@bot.message_handler(func=lambda message: message.chat.id != admin_chat, content_types=['photo'])
def get_user_photo(message):
    cid = message.chat.id
    try:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        image = config.image_path + str(cid) + '.jpg'
        with open(image, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(cid, 'Ok. photo has been grabbed')
        bot.send_photo(admin_chat, open(image, 'rb'), '{0}\n@{1}\n/say{2}'.format(message.chat.first_name,
                                                                                  message.chat.username,
                                                                                  message.chat.id))
        DataBase.db_insert(
            [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])

    except Exception:
        bot.send_message(cid, 'Sorry, photo has not grabbed')


@bot.edited_message_handler(func=lambda message: True)
def any_message(message):
    msg = message.text
    if msg.lower() in idinahoi_list:
        bot.reply_to(message, "Do not swear {!s}".format(msg))
    else:
        bot.send_message(admin_chat, msg)


@bot.message_handler(commands=['help'])
def receive_help_info(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Minerboard", url="https://minerboard.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, help_info, reply_markup=keyboard)
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])


@bot.message_handler(commands=['start'])
def start_dialogue(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    list_items = ['FAQ', ]
    for item in list_items:
        markup.add(item)
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])
    bot.send_message(message.chat.id, reply_markup=markup, text=greeting_info)


@bot.message_handler(func=lambda message: message.chat.id != admin_chat, regexp='FAQ')
def show_faq(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Minerboard FAQ", url="https://minerboard.com/faq.html")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, faq_message, reply_markup=keyboard)
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])


@bot.message_handler(func=lambda message: message.chat.id != admin_chat, content_types=['text'])
def receive_to_user(message):
    bot.send_message(admin_chat, '{0}\n{1}\n@{2}\nlang: {4}\n/say{3}'.format(message.text, message.chat.first_name,
                                                                             message.chat.username, message.chat.id,
                                                                             message.from_user.language_code))
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])
    bot.send_message(message.chat.id,
                     'Your request is confirmed. Our team will get in touch with you as soon as possible.')


@bot.message_handler(func=lambda message: message.chat.id != admin_chat, regexp='/\w*')
def ignore_user_command(message):
    bot.send_message(message.chat.id, 'Do not spam with commands :D\nMy father Cyber Defender!')
    DataBase.db_insert(
        [None, message.chat.first_name, message.chat.username, message.chat.id, message.from_user.language_code])


@bot.message_handler(func=lambda message: message.chat.id == admin_chat, regexp='/a.')
def get_admin_text(message):
    ''' через '/a ' пишем ответ для определенного пользователя '''
    msg = re.search('(?<=/a )(.*)', message.text)
    if not config.last_id:
        bot.send_message(admin_chat, 'Сообщение не отправлено.\nПользователь не найден')
    if config.last_id and msg:
        user = DataBase.db_select(config.last_id).fetchone()
        bot.send_message(admin_chat, 'Сообщение для пользователя: ' + str(config.last_id) + '\nnickname: ' +
                         user[1] + '\nusername: @' + user[2] + ' отправлено:\n' + msg.group(0))
        bot.send_chat_action(config.last_id, 'typing')  # show the bot "typing" (max. 5 secs)
        time.sleep(3)
        bot.send_message(config.last_id, msg.group(0))
        config.last_id = None


@bot.message_handler(func=lambda message: message.chat.id == admin_chat, regexp='/say.')
def choose_user(message):
    ''' через '/say\d+' выбираем кому пишем '''
    target_id = re.search('(?<=/say)(\d+)', message.text)
    if target_id:
        config.last_id = target_id.group(0)
        user = DataBase.db_select(target_id.group(0)).fetchone()
        bot.send_message(admin_chat, 'Напишите сообщение для: ' + target_id.group(0) + '\nnickname: ' +
                         user[1] + '\nusername: @' + user[2] + '\nДля ответа используйте /a text.')

    else:
        bot.send_message(admin_chat, 'None')


@bot.message_handler(func=lambda message: message.chat.id == admin_chat, commands=['users'])
def get_user_list(message):
    user_list = DataBase.db_select(full=1).fetchall()
    if user_list:
        for i in user_list:
            bot.send_message(admin_chat, 'nick: {0},\nusername: {1},\nid: /say{2},\nlang: {3}.\n'.format(
                i[1], i[2], i[3], i[4]))
    else:
        bot.send_message(admin_chat, 'No users detected or troubles occurred')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            print('error ', err)
            time.sleep(5)
