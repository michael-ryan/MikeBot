# Work with Python 3.6
import discord
import uuid as u
import time
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!mike ', help_command=None)

TOKEN = open("token.secret", "r").read()


@bot.command()
async def help(ctx):
    e = discord.Embed(title="MikeBot Help", description="Full MikeBot command reference", type="rich", color=0x00ff00)
    e.set_thumbnail(url="https://i.imgur.com/7uCNBtq.png")
    first = True
    with open("help.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("#"):
                if first:
                    first = False
                else:
                    e.add_field(name=name, value=value, inline=False)
                name=line.replace("#", "")
                value=""
            else:
                sp = line.split(": ")
                command = sp[0]
                action = sp[1]
                value += "- `!mike " + command + "` " + action
        e.add_field(name=name, value=value, inline=False)
    e.set_footer(text="Created by mehmenmike#4389")
    await ctx.channel.send(embed=e)


@bot.command()
async def uuid(ctx):
    await ctx.send("`" + str(u.uuid4()) + "`")


@bot.command()
async def invite(ctx):
    await ctx.send("https://tinyurl.com/sn5jnj9")
    # https://discordapp.com/oauth2/authorize?client_id=688534221324943360&permissions=67584&scope=bot


@bot.command()
async def epoch(ctx):
    await ctx.send("`" + str(int(time.time())) + "`")


@bot.command()
async def dad(ctx):
    URL = "https://icanhazdadjoke.com/"
    async with ctx.message.channel.typing():
        response = requests.get(URL, headers={"Accept": "application/json"})
        r = response.json()
        await san_send(ctx.message, r["joke"])


@bot.command()
async def fortune(ctx):
    URL = "http://yerkee.com/api/fortune"
    async with ctx.message.channel.typing():
        response = requests.get(URL)
        r = response.json()
        await san_send(ctx.message, r["fortune"])


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content == "!mike":
        await help(message)
    else:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name + " with ID#" + str(bot.user.id))
    print('-----------------------------------------------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! Use `!mike help` for a full command reference.")

async def san_send(message, text):
    text = text.replace("*", "\*")
    text = text.replace("_", "\_")
    text = text.replace("`", "\~")
    text = text.replace(">", "\>")
    await message.channel.send(text.format(message))

bot.run(TOKEN)