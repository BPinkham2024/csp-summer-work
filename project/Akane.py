import discord
from discord.ext import commands
import openai
import config

# bot init
intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# openai init
openai.api_key = config.AI_TOKEN

def chat_with_bot(message):
    prompt = f"You: {message}\nAkane Akemi:"

    response = openai.Completion.create(
        engine='text-davinci-003', 
        prompt=prompt,
        max_tokens=50, 
        temperature=0.7,
        n=1,
        stop=None,
        timeout=5
    )
    
    if response and response.choices:
        return response.choices[0].text.strip()
    else:
        return "Sorry, I couldn't generate a response at the moment."


# -------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('----')

@bot.event
async def on_message(message):
    user = str(message.author)
    user_msg = str(message.content)
    channel = str(message.channel.name)
    print(f'{user}: {user_msg} ({channel})')

    if message.author == bot.user:
        return
    
    if message.channel.name == 'general':
        if user_msg.lower() == 'hello':
            await message.channel.send(f'hello, {user}!')
        
        if user_msg.lower().startswith('>chat'):
            await message.channel.send(chat_with_bot(user_msg[5:]))


bot.run(config.BOT_TOKEN)