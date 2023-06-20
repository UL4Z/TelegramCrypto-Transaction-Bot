import logging
import time
import requests
from telebot import TeleBot
from telebot.types import Update, InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot("put your bot token here")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@bot.message_handler(commands=['status'])
def status(message):
    try:
        if len(message.text.split()) < 2:
            raise ValueError(
                'Please provide a transaction hash. Use the command in this format: /status <transaction_hash>')

        transaction_hash = message.text.split()[1]
        print(f'{message.from_user.username} - {message.from_user.id} -> /status {transaction_hash}')

        r = requests.get(f'https://mempool.space/api/tx/{transaction_hash}/status')
        r.raise_for_status()  # Raise an exception for non-200 status codes

        data = r.json()
        confirmed = data['confirmed']
        if confirmed:
            response = f'Transaction🏷️💲 {transaction_hash} confirmed'
        else:
            response = f'Transaction❌🚫 {transaction_hash} not confirmed'
        bot.send_message(chat_id=message.chat.id, text=response)

    except ValueError as e:
        bot.send_message(chat_id=message.chat.id, text=str(e))

    except requests.RequestException:
        bot.send_message(chat_id=message.chat.id, text='An error occurred while attempting to make the API request.')

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text='An unexpected error occurred.')
        logging.exception(e)


@bot.message_handler(commands=['watch'])
def watch(message):
    try:
        message_parts = message.text.split()
        if len(message_parts) < 2:
            raise ValueError(
                'Please provide a transaction hash. Use the command in this format: /watch <transaction_hash>')

        transaction_hash = message_parts[1]
        print(f'{message.from_user.username} - {message.from_user.id} -> /watch {transaction_hash}')

        bot.send_message(chat_id=message.chat.id,
                         text='I will notify you 🕐 when this transaction has reached 1 confirmation!')

        while True:
            try:
                r = requests.get(f'https://mempool.space/api/tx/{transaction_hash}/status')
                r.raise_for_status()  # Raise an exception for non-200 status codes

                data = r.json()
                confirmed = data['confirmed']
                if confirmed:
                    response = f'`{transaction_hash}` has reached 1 confirmation!'
                    bot.send_message(chat_id=message.chat.id, text=response)
                    break
                time.sleep(60)

            except requests.RequestException:
                bot.send_message(chat_id=message.chat.id,
                                 text='An error occurred while attempting to make the API request.')
                break

            except Exception as e:
                bot.send_message(chat_id=message.chat.id, text='An unexpected error occurred.')
                logging.exception(e)
                break

    except ValueError as e:
        bot.send_message(chat_id=message.chat.id, text=str(e))

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text='An unexpected error occurred.')
        logging.exception(e)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Welcome to the Crypto Transactional Monitoring Bot! Type /help for more information on how to use this bot.")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,
                 "The list of commands are as follows:\n ✔️ /start\n 🛑 /help\n ✅ /status <transaction_hash>\n 🕐 /watch <transaction_hash>")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Unrecognized command. To start the bot, type /start")


bot.infinity_polling()

#clammbon :)
