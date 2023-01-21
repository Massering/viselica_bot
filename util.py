import telebot
import pymorphy2
import pymorphy2_dicts_ru


def keyboard(values: iter, one_time=True) -> telebot.types.ReplyKeyboardMarkup:
    """Возвращает клавиатуру, содержащую кнопки со значениями values"""
    my_keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=one_time)
    for value in values:
        key1 = telebot.types.KeyboardButton(value)
        my_keyboard.add(key1)
    return my_keyboard


def bool_keyboard(one_time=True) -> telebot.types.ReplyKeyboardMarkup:
    """Возвращает клавиатуру, состоящую из кнопок 'Да' и 'Нет'"""
    my_keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=one_time)
    my_keyboard.add(telebot.types.KeyboardButton('Да'), telebot.types.KeyboardButton('Нет'))
    return my_keyboard


def reform(word: str, n: int) -> str:
    """Возвращает слово, измененное под числительное, переданное вторым параметром"""
    if word == 'будет':
        if n == 1:
            return word
        return 'будут'

    pymorphy2_dicts_ru.get_path()
    # Чтобы изменять слова по числительным
    morph = pymorphy2.MorphAnalyzer()

    word_form: pymorphy2.analyzer.Parse = morph.parse(word)[0]
    return word_form.make_agree_with_number(n).word


def log(func):
    """Это декоратор"""
    def new_func(message: telebot.types.Message, *args, **kwargs):
        print(message.from_user.id, ': ', message.text, sep='')
        return func(message, *args, **kwargs)

    return new_func
