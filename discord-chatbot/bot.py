import os
from dotenv import load_dotenv
import discord
import requests

load_dotenv()  # Laden der .env Datei

client = discord.Client(intents=discord.Intents.default())

OLLAMA_API = os.getenv('OLLAMA_API')
conversation_history = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{client.user.id}>', '').strip()
        try:
            response = get_ollama_response(prompt, str(message.author.id))
            await message.reply(response)
        except Exception as e:
            print('Error:', e)
            await message.reply('Sorry, an error occurred.')

def get_ollama_response(prompt, user_id):
    data = {
        'model': 'qwen:0.5b',
        'messages': conversation_history.get(user_id, [{'role': 'user', 'content': prompt}])
    }

    response = requests.post(f'{OLLAMA_API}/chat/completions', json=data)
    response_data = response.json()

    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({'role': 'user', 'content': prompt})
    conversation_history[user_id].append(response_data['choices'][0]['message'])

    return response_data['choices'][0]['message']['content']

client.run(os.getenv('DISCORD_TOKEN'))
