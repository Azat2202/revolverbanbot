import random

from aiogram import Bot, Dispatcher, executor, types
from get_users import users
from emoji import emojize
from random import randint, choice
from time import sleep, time
from wishes import get_wishes
import datetime

API_TOKEN = '5098673114:AAHTLpXaLEBKsVyZChzzDO0u1_B2OqflwfQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
wait_seconds = 150
wait_seconds_for_horo = 30000
wait_seconds_for_mention = 5000
last_time_banned = datetime.datetime.now() - datetime.timedelta(seconds=wait_seconds)
last_time_horo = datetime.datetime.now() - datetime.timedelta(days=1)
last_time_mentioned = datetime.datetime.now() - datetime.timedelta(seconds=wait_seconds_for_mention)
massive = [1 for i in users]


# -1001458827756
def form_repr(num):
    global massive
    pistol = emojize(":water_pistol:")
    out = ''
    if num == -1:
        for person in users:
            out += f'{pistol}{person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
    else:
        for per_num, person in enumerate(users):
            if massive[per_num] == 1:
                out += f'{pistol}{person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
            else:
                out += f'— {person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
    return out


@dp.message_handler(commands=['horo_for_all'])
async def solo_horo(message: types.Message):
    global last_time_horo
    now_time = datetime.datetime.now()
    delta = now_time - last_time_horo
    out = ''
    if delta.seconds > wait_seconds_for_horo or delta.days > 0:
        last_time_horo = now_time
        for person in users:
            today_horo = get_wishes(users)
            out += f'[{person.name}](tg://user?id={person.user_id}){choice(today_horo)}\n'
        await bot.send_message(message.chat.id, out, parse_mode='Markdown', reply_to_message_id=message.message_id)
    else:
        await bot.send_message(message.chat.id,
                               f'До использования команды заново осталось {(wait_seconds_for_horo - delta.seconds) // 3600} часов')


@dp.message_handler(commands=['mark_all'])
async def mark_all(message: types.Message):
    global last_time_mentioned
    now_time = datetime.datetime.now()
    delta = now_time - last_time_mentioned
    out = ''
    if delta.seconds > wait_seconds_for_mention or delta.days > 0:
        last_time_mentioned = now_time
        out += f'{message.from_user.first_name} ОРГАНИЗОВАЛ ВСЕОБЩИЙ СБОР\n'
        for person in users:
            out += f'[{person.name}](tg://user?id={person.user_id})  '
        await bot.send_message(message.chat.id, out, parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id,
                               f'До использования команды заново осталось {(wait_seconds_for_mention - delta.seconds) // 3600} часов')


@dp.message_handler(commands=['horo'])
async def all_horo(message: types.Message):
    today_horo = get_wishes(users)
    out = f'{message.from_user.first_name}{"" if message.from_user.last_name is None else " " + str(message.from_user.last_name)}{choice(today_horo)}'
    await bot.send_message(message.chat.id, out, reply_to_message_id=message.message_id)


@dp.message_handler(commands=['ban'])
async def kill_sbd(message: types.Message):
    global last_time_banned, massive
    now_time = datetime.datetime.now()
    delta = now_time - last_time_banned
    if delta.seconds > wait_seconds or delta.days > 0:
        massive = [1 for i in users]
        last_time_banned = now_time
        last_message = await message.reply(form_repr(-1))
        num_to_ban = randint(0, len(users) - 1)
        while sum(massive) != 1:
            sleep(sum(massive) / 100)
            num1 = randint(0, len(users) - 1)
            while num1 == num_to_ban or massive[num1] == 0:
                num1 = randint(0, len(users) - 1)
            num2 = randint(0, len(users) - 1)
            while num2 == num_to_ban or massive[num2] == 0:
                num2 = randint(0, len(users) - 1)
            massive[num1] = 0
            massive[num2] = 0
            await bot.edit_message_text(form_repr(num_to_ban), message.chat.id, last_message.message_id)
        sleep(4)
        await bot.edit_message_text(
            f'{users[num_to_ban].name} {"" if users[num_to_ban].surname is None else " " + str(users[num_to_ban].surname) + " "}забанен на 5 минут{emojize(":smiling_face_with_horns:")}',
            message.chat.id, last_message.message_id)
        await bot.restrict_chat_member(message.chat.id, users[num_to_ban].user_id, can_send_messages=False,
                                       until_date=int((time() + 300)))
    else:
        await bot.send_message(message.chat.id,
                               f'До использования команды заново осталось {wait_seconds - delta.seconds} секунд')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
