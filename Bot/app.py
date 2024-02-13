import telebot
from config import TOKEN, keys
from extensions import ConvertionExeption, APIException


bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'
@bot.message_handler(commands=['start', 'help'])

def help(message: telebot.types.Message):
    text = ('Что бы произвести расчет введите данные в формате: \n <переводимая валюта> \n '
'<во что переводим> \n <кол-во> \nТак же можно запросить список доступных валют /values')
    bot.reply_to(message, text)

def handle_start(message):
    pass

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')  # введеное сообщение делим по пробелам

        if len(values) != 3:  # если много значачений, уведомляем об ошибке
            raise ConvertionExeption('Не корректное кол-во параметров')
        quote, base, amount = values  # присваиваем переменным значения из сообщения
        total_base = APIException.convert(quote, base, amount)            #json.loads(r.content)[keys[base]]
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n {e}')
    else:
        total_base_2 = round(total_base, 2)
        text = f'Цена {amount} {quote} - {total_base_2} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()

