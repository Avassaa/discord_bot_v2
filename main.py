from typing import Final
import os

import discord
from dotenv import load_dotenv
from discord import Intents,Client,Message
from discord.ext import commands
from responses import get_response
from datetime import datetime
import music_cog


isChatGPT:bool=True
#STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN:Final[str]=os.getenv('DISCORD_TOKEN')
# STEP 1 : BOT SETUP
intents: Intents=Intents.default()
intents.message_content=True # NOQA
client:Client = Client(intents=intents)



# STEP2: MESSAGE FUNCTIONALITY

async def send_message(message:Message,user_message:str)->None:
    if not user_message:
        print('(Message was empty')
        return
    if is_private:=user_message[0:2]=="$$":
        user_message=user_message[2:]
    elif user_message[0]=="$":
        is_private=False
        user_message=user_message[1:]
    else :
        return

    try:
        response:str =get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#STEP 3: HANDLING STARTUP
@client.event
async def on_ready() -> None:

    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) ->None:
    global isChatGPT
    if message.author==client.user: #if it's the bot who sent the message , ignore
        return
    if message.content.startswith("$loop"):
        isChatGPT=False
        await music_cog.toggle_loop(message)
    if message.content.startswith("$play") or message.content.startswith("$pause"):
        isChatGPT=False
        await music_cog.play_music(message)
    if message.content.startswith("$exit") or message.content.startswith("$disconnect") or message.content.startswith("$fuckoff"):
        isChatGPT = False
        await music_cog.disconnect(message)
    if message.content.startswith("$resume"):
        isChatGPT=False
        await music_cog.play_music(message)


    username: str=str(message.author)
    user_message:str =message.content
    channel:str=str(message.channel)

    print(f'[{channel}] {username}: {user_message}')
    with open('server_log.txt', 'a') as log:
        # Write content to the file
        current_time = datetime.now()
        log.write(f'[{channel}] {username}: {user_message} at {current_time}\n')

    if(isChatGPT):
        await send_message(message,user_message)

#STEP 5:MAIN ENTRY POINT
def main()->None:
    client.run(token=TOKEN)

if __name__ =='__main__':
    main()
