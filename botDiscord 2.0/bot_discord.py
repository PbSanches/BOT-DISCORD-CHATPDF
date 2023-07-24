import discord
import requests
import asyncio
DISCORD_TOKEN = "" #token do seu bot
CHATPDF_API_KEY = "" #sua key do chat pdf
SOURCE_ID = ""  #id fonte do seu pdf
CHANNEL_ID = ""  # Replace YOUR_CHANNEL_ID with the actual channel ID

def send_message(message):
    url = "https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": "Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "content": message,
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

def get_chatpdf_response(question):
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {
        "x-api-key": CHATPDF_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "sourceId": SOURCE_ID,
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["content"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!pdf'):
        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            question_message = await client.wait_for('message', check=check, timeout=60)
            question = question_message.content.strip()

            chatpdf_response = get_chatpdf_response(question)
            await message.channel.send(chatpdf_response)
        except asyncio.TimeoutError:
            await message.channel.send("Tempo limite excedido. Tente novamente.")

client.run(DISCORD_TOKEN)