import telebot
import time
import os
from threading import Thread

ver = 'beta 0.1'
folder = ''

bot = telebot.TeleBot('')  # bot token
message_text_file_name_timer = 'Первый запуск'
chat_id = ''


# определяет путь к папке folder
def folder_path(folder):
    current_dir = os.getcwd()  # Получаем путь к текущей папке
    path = os.path.join(current_dir, folder)  # получаем путь к папке folder
    return path


# Получаем список всех файлов в папке folder
def file_list(folder):
    files_list = [f for f in os.listdir(folder_path(folder))]
    return files_list


# создаем файл в папке с текстом
def new_file(file_name, folder, text):
    path = folder_path(folder)
    with open(os.path.join(path, file_name), 'w') as file:
        file.write(text)
        message_for_user = f'файл {file_name} создан.'
    return message_for_user


# удаляет файл в папке
def delete_file(file_name, folder):  # удаляет файл в папке
    path = folder_path(folder)
    file_path = os.path.join(path, file_name)  # объединяет path и filename
    if os.path.exists(file_path):  # Проверяем существует ли файл
        os.remove(file_path)  # Удаляем файл
        message_for_user = (f"Файл {file_name} удалён.")  # Выводим сообщение, что файл удалён
    else:
        message_for_user = (f"Файл {file_name} не найден.")  # Выводим сообщение, что файл не найден
    return message_for_user


# считывает содержимое файла file_name из папки folder
def read_in_folder_file_name(folder, file_name):
    if os.path.exists(os.path.join(folder_path(folder), file_name)):
        with open(os.path.join(folder_path(folder),
                               file_name)) as f:  # открываем файл, блок with, который гарантирует автоматическое закрытие файла после выхода из блока
            file_content = f.read()
            file_content = file_content.strip()
    else:
        file_content = ("Файл не найден.")
    return file_content


# текущее время в формате 0000 str
def check_time():
    hour = str(time.localtime().tm_hour)
    if len(hour) == 1:
        hour = '0' + str(hour)
    min = str(time.localtime().tm_min)
    if len(min) == 1:
        min = '0' + min
    t = hour + min
    return str(t)


# при совпадении времени с именем файла заменяет значение глобальной переменной message_text_file_name_timer на текст из файла
def loop_check_time_file_message():
    global message_text_file_name_timer
    global folder
    check_message = ''
    while True:
        time.sleep(3)
        time_now = check_time()
        file_name = time_now
        answer_def = read_in_folder_file_name(folder, file_name)
        if answer_def != ("Файл не найден."):
            message_text_file_name_timer = answer_def
            print(message_text_file_name_timer)
            time.sleep(5)
            if check_message != message_text_file_name_timer:
                bot.send_message(chat_id, message_text_file_name_timer)
                check_message = message_text_file_name_timer


@bot.message_handler()
def check(message):  # проверка сообщений
    global message_text_file_name_timer
    global folder

    help_text = read_in_folder_file_name(folder, 'help.txt')
    message_text = message.text

    if message.text == '/help':  # выдаем помощ из файла help.txt
        bot.send_message(message.chat.id, help_text)
    if message.text == '/start':  # запуск бота
        file_name = 'comand.txt'
        answer_def = read_in_folder_file_name(folder, file_name)
        bot.send_message(message.chat.id, f'Версия: {ver}, \n{answer_def}')
    if message.text == '/id':  # выдаёт ID чата в чат
        bot.send_message(message.chat.id, f'Ваш чат id: {message.chat.id}')
        print(f'id: {message.chat.id}')
    if message.text == '/last':  # Выдает текст последнего сработавшего таймера
        bot.send_message(message.chat.id, f'Последний таймер: {message_text_file_name_timer}')
    if message.text == '/list':  # Выдает список файлов
        bot.send_message(message.chat.id, f'Список файлов: {file_list(folder)}')
    if message.text.startswith('/read '):  # /read имя файла выдает содержимое файла
        file_name = message.text.split(' ')[1]
        answer_def = read_in_folder_file_name(folder, file_name)
        bot.send_message(message.chat.id, answer_def)
    if message.text == '/ver':  # Выдает версию бота
        bot.send_message(message.chat.id, f'Версия: {ver}')

    else:
        number = ''
        for symbol in message_text[:4]:
            if symbol.isdigit():
                number += symbol
            if len(number) == 4:
                break

        if len(number) == 4 and len(message_text) > 6:
            answer_def = new_file(file_name=number, folder=folder, text=message_text)
            bot.send_message(message.chat.id, answer_def)
            time.sleep(1)
        if len(number) == 4 and len(message_text) < 6:
            answer_def = delete_file(file_name=number, folder=folder)
            bot.send_message(message.chat.id, answer_def)
            time.sleep(1)


message_timer = Thread(target=loop_check_time_file_message)
message_timer.start()

time.sleep(3)
bot.polling(none_stop=True)
