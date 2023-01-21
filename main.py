import telebot
import requests
import time

from config import *
from util import *

bot = telebot.TeleBot(TOKEN)


def make_message(word: str, letters: list) -> str:
    s = word
    print(s, letters)
    for i in s:
        if i not in letters:
            s = s.replace(i, '_')
    mistakes = len(set(letters) - set(s))
    print(s, mistakes)

    s += '\n'
    s += '\n'.join(" ".join([j + STRIKETHROUGH if j in letters else j for j in i]) for i in ALF)
    s += '\n'
    s += VISELICA[mistakes]
    print(s)

    return s


@log
@bot.message_handler(commands=['rules'])
def rules(message: telebot.types.Message):
    bot.send_message(message.chat.id, '''Правила:
Виселица (также «Балда») — игра на бумаге для двух (или больше) человек.
Принцип игры
Один из игроков загадывает слово — пишет на бумаге любые две буквы слова и отмечает места для остальных букв, например чертами (существует также вариант, когда изначально все буквы слова неизвестны). Также рисуется виселица с петлёй.
Согласно традиции русских лингвистических игр, слово должно быть именем существительным, нарицательным в именительном падеже единственного числа, либо множественного числа при отсутствии у слова формы единственного числа.
Второй игрок предлагает букву, которая может входить в это слово. Если такая буква есть в слове, то первый игрок пишет её над соответствующими этой букве чертами — столько раз, сколько она встречается в слове. Если такой буквы нет, то к виселице добавляется круг в петле, изображающий голову. Второй игрок продолжает отгадывать буквы до тех пор, пока не отгадает всё слово. За каждый неправильный ответ первый игрок добавляет одну часть туловища к виселице (обычно их 6: голова, туловище, 2 руки и 2 ноги, существует также вариант с 8 частями — добавляются ступни, а также самый длинный вариант, когда сначала за неотгаданную букву рисуются части самой виселицы).
Если туловище в виселице нарисовано полностью, то отгадывающий игрок проигрывает, считается повешенным. Если игроку удаётся угадать слово, он выигрывает и может загадывать слово.''')


@log
@bot.message_handler()
def start(message: telebot.types.Message):
    if message.from_user.id in people:
        chat = people[message.from_user.id]
        if chat == message.chat.id:
            bot.send_message(message.chat.id, 'В личку, дурак!\n@viselica_bot')
        elif message.text == '/start':
            bot.send_message(message.chat.id, 'Окей, а теперь пришли мне слово')
        else:
            chats[chat] = (message.text.upper(), [])
            bot.send_message(chat, make_message(*chats[chat]))
        return

    bot.send_message(message.chat.id, 'Привет! Кто будет отгадывать?')
    bot.register_next_step_handler(message, begin, set())


@log
def begin(message: telebot.types.Message):
    people[message.from_user.id] = message.chat.id

    bot.send_message(message.chat.id, f'Отлично, {message.from_user.full_name}, а теперь отправь мне в лс слово!')


if __name__ == '__main__':
    chats = {}
    people = {}

    while 1:
        try:
            print('Start')
            # Запускаем бота
            bot.polling(non_stop=True, skip_pending=True)

        except Exception as log_error:
            if isinstance(log_error, requests.exceptions.ReadTimeout):
                # Такие ошибки могут появляться регулярно
                # Я читал, их возникновение связано с ошибками в библиотеке telebot
                print('That annoying errors erroring again')

            elif isinstance(log_error, requests.exceptions.ConnectionError):
                # Такое чаще всего при отсутствии подключения к интернету
                print('Ошибка соединения. Проверьте подключение к интернету')

            else:
                # Иначе отправляем админу, чтобы он разбирался
                print('Polling error: ' + f'({log_error.__class__}, {log_error.__cause__}): {log_error}')
            time.sleep(5)