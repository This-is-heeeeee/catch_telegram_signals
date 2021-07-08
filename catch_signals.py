from telethon import TelegramClient, events
import subprocess
import configparser
import json
import re

api_id = ''
api_hash = ''

channel = ''

firstFilter = ['hit']# 'hit'이 있으면 x
subjectFilter = ['signal', 'call']
levelFilter = ['Buy', 'Entry' 'target']
symbolFilter = ['#', '$', '/usdt']

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel))
async def newMessageListener(event):
    newMessage = event.message.message

    firstFiltered = re.findall(r"(?=("+'|'.join(firstFilter)+r"))", newMessage, re.IGNORECASE)

    if not firstFiltered:
        subjectFiltered = re.findall(r"(?=("+'|'.join(subjectFilter)+r"))", newMessage, re.IGNORECASE)#re.IGNORECASE 대소문자 구분 x

        if subjectFiltered:
            print("sub : {}".format(subjectFiltered))
            levelFiltered = re.findall(r"(?=("+'|'.join(levelFilter)+r"))", newMessage, re.IGNORECASE)

            if levelFiltered:
                print("lev : {}".format(levelFiltered))
                symbolFiltered = re.findall(r"(?=("+'|'.join(symbolFilter)+r"))", newMessage, re.IGNORECASE)
                if symbolFiltered:
                    print("sym : {}".format(symbolFiltered))
                    symbol = ''
                    if symbolFiltered[0] == '/usdt':
                        messages = newMessage.split(symbolFiltered[0])
                        messages = messages[0].split()
                        symbol = messages[-1] + '/usdt'

                    else:
                        messages = newMessage.split(symbolFiltered[0])
                        messages = messages[-1].split()
                        symbol = messages[0] + '/usdt'

                    print("symbol : {}".format(symbol))
                    subprocess.call(f'python market_order {symbol}', shell=True)

with client:
    client.run_until_disconnected()
