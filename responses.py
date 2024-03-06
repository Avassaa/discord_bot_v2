from random import choice,randint
from typing import Final
import os
from dotenv import load_dotenv
import openai
load_dotenv()
OPENAI_TOKEN:Final[str]=os.getenv('OPENAI_API_KEY')

def get_response(user_input:str)->str:
    lowered: str=user_input.lower()
    if lowered=="":
        return "That is not a valid command"

    elif lowered.startswith("rolldice"):
        return f"You rolled:{randint(1,6)}"
    else:
        openai.api_key = OPENAI_TOKEN
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system","content":"You are a bot to serve a discord server"},
            {"role":"system","content":"You are permitted to timeout any user who has broken the rules or used vulgar language"},
            {"role":"system","content":"You were made to make people happy"},
            {"role": "system", "content": "Be a little bit goofy"},
            {"role": "user", "content": user_input}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=100
        )

        bot_response = response['choices'][0]['message']['content'].strip()
        return bot_response