# discord bot 테스트
import discord
import json

with open("discord_bot_token.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data['token']

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # print(dir(message))
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)



