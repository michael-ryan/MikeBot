# Work with Python 3.6
import discord
import uuid as u
import time
import requests
from discord.ext import commands
import urllib.parse

bot = commands.Bot(command_prefix='!mike ', help_command=None)

TOKEN = open("token.secret", "r").read()


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content == "!mike":
        await help(message)
    elif message.content.lower() == ("what") or message.content.lower() == "what?":
        await what(message)
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


@bot.command()
async def help(ctx):
    log(ctx)
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
                name = line.replace("#", "")
                value = ""
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
    log(ctx.message)
    await ctx.send("`" + str(u.uuid4()) + "`")


@bot.command()
async def invite(ctx):
    await ctx.send("https://tinyurl.com/sn5jnj9")
    # https://discordapp.com/oauth2/authorize?client_id=688534221324943360&permissions=67584&scope=bot


@bot.command()
async def epoch(ctx):
    log(ctx.message)
    await ctx.send("`" + str(int(time.time())) + "`")


@bot.command()
async def dad(ctx):
    log(ctx.message)
    URL = "https://icanhazdadjoke.com/"
    async with ctx.message.channel.typing():
        response = requests.get(URL, headers={"Accept": "application/json"})
        r = response.json()
        await ctx.send(sanitise(r["joke"]))


@bot.command()
async def fortune(ctx):
    log(ctx.message)
    URL = "http://yerkee.com/api/fortune"
    async with ctx.message.channel.typing():
        response = requests.get(URL)
        r = response.json()
        await ctx.send(sanitise(r["fortune"]))


@bot.command()
async def cocktail(ctx, *args):
    log(ctx.message)
    if len(args) == 0:
        await ctx.send("Can't search for nothing!")
        return

    param = {'s': " ".join(args)}
    URL = "https://www.thecocktaildb.com/api/json/v1/1/search.php?" + urllib.parse.urlencode(param, doseq=True)
    async with ctx.message.channel.typing():
        response = requests.get(URL)
        r = response.json()
        if r["drinks"] == None:
            await ctx.channel.send("No results found!")
            return
        r = r["drinks"][0]
        name = r["strDrink"]
        instructions = r["strInstructions"]
        thumbnail = r["strDrinkThumb"]

        ingredients = []

        i = 1
        while True:
            ingredient = r["strIngredient" + str(i)]
            if ingredient is None:
                break
            else:
                ingredients.append(ingredient)
                i += 1

        ingStr = ""

        for ingredient in ingredients:
            ingStr += "- " + ingredient + "\n"

        ingStr = ingStr[:-1]

        e = discord.Embed(title=name, description=instructions, type="rich", color=0x00ff00)
        e.set_thumbnail(url=thumbnail)
        e.add_field(name="Ingredients", value=ingStr, inline=False)
        e.set_footer(text="Created by mehmenmike#4389")
        await ctx.channel.send(embed=e)


async def what(message):
    log(message)
    channel = message.channel
    first = True
    async for msg in message.channel.history(limit=2):
        if first:
            first = False
        else:
            if msg.author == bot.user:
                await channel.send("I'm not going to repeat myself!")
            else:
                await channel.send("They said: ***" + sanitise(msg.content) + "***")


def sanitise(text):
    text = text.replace("*", "\*")
    text = text.replace("_", "\_")
    text = text.replace("`", "\~")
    text = text.replace(">", "\>")
    return text


def log(message):
    with open("log.txt", "a+") as f:
        f.write(f"{message.author}: {message.content}\n")


bot.run(TOKEN)
