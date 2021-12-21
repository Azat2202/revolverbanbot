from telethon import TelegramClient, events, sync
from dataclasses import dataclass, field
import sys
import os
import time

API_TOKEN = '5098673114:AAHTLpXaLEBKsVyZChzzDO0u1_B2OqflwfQ'
users = []
channel_id = -1001458827756


@dataclass(order=True)
class user:
    user_id: int
    name: str
    surname: str
    username: str


def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


client = TelegramClient('session_name', 14494169, 'be46953bb44aec0cd51a8241e310d06e').start(bot_token=API_TOKEN)
client.start()
count = 0
for participant in client.get_participants(channel_id):
    if not participant.bot:
        users.append(user(participant.id, participant.first_name, participant.last_name, participant.username))
# for participant in client.iter_participants(channel_id, aggressive=True):
#     users.append(user(participant.id, participant.first_name, participant.last_name))
client.disconnect()
users.sort()