from aiogram import Bot, Dispatcher, executor, types
from get_users import users
from emoji import emojize
from random import randint
from time import sleep, time
import datetime

API_TOKEN = '5098673114:AAHTLpXaLEBKsVyZChzzDO0u1_B2OqflwfQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
wait_seconds = 1800
last_time_banned = datetime.datetime.now() - datetime.timedelta(seconds=wait_seconds)


# -1001458827756
def form_repr(num):
    out = ''
    if num == -1:
        for person in users:
            out += f'— {person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
    else:
        for per_num, person in enumerate(users):
            if per_num != num:
                out += f'— {person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
            else:
                out += f'{emojize(":water_pistol:")}{person.name}{"" if person.surname is None else " " + str(person.surname)},\n'
    return out


@dp.message_handler(commands=['ban'])
async def kill_sbd(message: types.Message):
    global last_time_banned
    now_time = datetime.datetime.now()
    delta = now_time - last_time_banned
    if delta.seconds > wait_seconds or delta.days > 0:
        last_time_banned = now_time
        last_message = await message.reply(form_repr(10))
        num_to_ban = randint(0, len(users) - 1)
        for i in range(0, len(users) + num_to_ban + 1):
            sleep(i / 90)
            await bot.edit_message_text(form_repr(i % len(users)), message.chat.id, last_message.message_id)
        sleep(1)
        await bot.edit_message_text(
            f'{users[num_to_ban].name} {"" if users[num_to_ban].surname is None else " " + str(users[num_to_ban].surname) + " "}забанен на час{emojize(":smiling_face_with_horns:")}',
            message.chat.id, last_message.message_id)
        await bot.kick_chat_member(message.chat.id, users[num_to_ban].user_id, int(time() + 3600))
    else:
        await bot.send_message(message.chat.id,
                               f'До использования команды заново осталось {wait_seconds - delta.seconds} секунд')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
