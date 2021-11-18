import telebot
import extensions
import config


bot = telebot.TeleBot(config.TOKEN)



# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id,'Для введённой суммы денег в одной валюте бот сообщает соответствующую сумму денег в другой валюте.Для получения информации о работе бота ввести команду /start или /help.Для вывода информации о всех доступных валютах ввести команду /values.Для того ,чтобы узнать для введённой суммы денег в одной валюте  соответствующую сумму денег в другой валюте нужно ввести следующий текст: <имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>.')

# Обрабатываются все сообщения, содержащие командy '/values'.
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    bot.send_message(message.chat.id,'Бот работает со следующими валютами:доллар(вводить - USD),евро(вводить - EUR) и рубль (вводить - RUR)')

# Обрабатываются все текстовые сообщения,не содержащие команд
@bot.message_handler(content_types=['text'])
def handle_mess(message: telebot.types.Message):
    #разбиваем текст сообщения на подстроки
    L = message.text.split()
    #проверяем текст сообщения


    try:
        if len(L) != 3:
            raise extensions.APIException(config.ARGS_QUANTITY_Text_Error)
    except extensions.APIException:
        bot.send_message(message.chat.id, config.ARGS_QUANTITY_Text_Error)
        return
    try:
        if L[0] == 'EUR' or L[0] =='USD' or L[0] =='RUR':
            pass
        else:
            raise extensions.APIException(config.FIRST_ARG_Text_Error)
    except extensions.APIException:
            bot.send_message(message.chat.id, config.FIRST_ARG_Text_Error)
            return

    try:
        if L[1] == 'EUR' or L[1] =='USD' or L[1] =='RUR':
            pass
        else:
            raise extensions.APIException(config.SECOND_ARG_Text_Error)
    except extensions.APIException:
            bot.send_message(message.chat.id, config.SECOND_ARG_Text_Error)
            return

    try:
        if L[2].isalpha() == True:
            raise extensions.APIException(config.THIRD_ARG_Text_Error)
        else:
            if L[2].isdigit()  == True:
                val = int(L[2])
                pass
            else:
                if 0 == L[2].find('.') or len(L[2]) == (1 + L[2].find('.')):
                    raise extensions.APIException(config.THIRD_ARG_Text_Error)
                try:
                    val = float(L[2])
                except ValueError:
                    bot.send_message(message.chat.id, config.THIRD_ARG_Text_Error)
                    return
    except extensions.APIException:
            bot.send_message(message.chat.id, config.THIRD_ARG_Text_Error)
            return
    try:
        if type(val) == 'int':
            if val < 0:
                raise extensions.APIException(config.THIRD_ARG_Text_Error)
        else:
            if val < 0.0:
                raise extensions.APIException(config.THIRD_ARG_Text_Error)
    except:
        bot.send_message(message.chat.id, config.THIRD_ARG_Text_Error)
        return

    #отправляем запрос на сервер
    r = extensions.cryptoAPI.get_price(L[0],L[1],val)
    if r['error'] == -1:
        bot.send_message(message.chat.id, config.THIRD_ARG_Text_Error)
        return
    else:
        if r['error'] == -2:
            bot.send_message(message.chat.id, config.REQ_API_Error)
            return

    #отправляем сообщение пользователю с информацией о сумме денег
    bot.send_message(message.chat.id,str(r['value']))

bot.polling(none_stop=True)

