import discord
from discord.ext import commands
from discord import app_commands
import openai
import config

# bot init
bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())
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
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    
# @bot.tree.command(name = 'test', description="This is a dest Command")
# async def test(interaction: discord.Interaction):
#     # await interaction.response.send_message(f'This is a test, {interaction.user.mention}', ephemeral=True)
#     """Test Desc"""
#     await interaction.response.send_message(f'This is a test, {interaction.user.mention}')
    
    
# gpt chatbot commands
@bot.tree.command(name="chat", description="Chat with Akane Akemi!")
@app_commands.describe(msg = "msg")
async def chat(interaction: discord.Interaction, msg: str):
    # await interaction.response.send_message(chat_with_bot(arg), ephemeral=True)
    await interaction.response.send_message(chat_with_bot(msg))
    
@bot.tree.command(name="embedded-chat", description="Chat with Akane Akemi but she will responed in an embed.")
@app_commands.describe(msg = "msg")
async def chatEmbed(interaction: discord.Interaction, msg: str):
    # embed = discord.Embed(title='Akane Akemi', description=chat_with_bot(msg), color=0x00FF22)
    await interaction.response.send_message(embed=discord.Embed(title='Akane Akemi', description=chat_with_bot(msg), color=0xff748c))


@bot.event
async def on_message(message):
    try:
        user = str(message.author)
        user_msg = str(message.content)
        channel = str(message.channel.name)
        print(f'{user}: {user_msg} ({channel})')
    except Exception as e:
        print('**hidden message**')

    if message.author == bot.user:
        return
    
    if message.channel.name == 'general':
        if user_msg.lower() == 'hello':
            await message.channel.send(f'hello, {user}!')
        
        if user_msg.lower().startswith('>chat'):
            await message.channel.send(chat_with_bot(user_msg[5:]))


bot.run(config.BOT_TOKEN)