# Work with Python 3.6
import discord
import uuid
import time
import requests

TOKEN = open("token.secret", "r").read()

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith("!mike"):
        messagecontent = message.content.lower().split(" ")
        if len(messagecontent) == 1:
            await display_command_reference(message)
        else:
            if messagecontent[1] == "help":
                await display_command_reference(message)
            elif messagecontent[1] == "uuid":
                await message.channel.send(("`" + str(uuid.uuid4()) + "`").format(message))
            elif messagecontent[1] == "invite":
                await message.channel.send("https://tinyurl.com/sn5jnj9".format(message))
            elif messagecontent[1] == "epoch":
                await message.channel.send(("`" + str(int(time.time())) + "`").format(message))
            elif messagecontent[1] == "dad":
                URL = "https://icanhazdadjoke.com/"
                async with message.channel.typing():
                    response = requests.get(URL, headers={"Accept": "application/json"})
                    r = response.json()
                    await san_send(message, r["joke"])
            elif messagecontent[1] == "fortune":
                URL = "http://yerkee.com/api/fortune"
                async with message.channel.typing():
                    response = requests.get(URL)
                    r = response.json()
                    await san_send(message, r["fortune"])
            else:
                await message.channel.send("Command not found! Use `!mike help` for a full command reference.".format(message))


@client.event
async def on_ready():
    print("Logged in as " + client.user.name + " with ID#" + str(client.user.id))
    print('-----------------------------------------------')


async def display_command_reference(message):
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
    await message.channel.send(embed=e)

async def san_send(message, text):
    text = text.replace("*", "\*")
    text = text.replace("_", "\_")
    text = text.replace("`", "\~")
    text = text.replace(">", "\>")
    await message.channel.send(text.format(message))

client.run(TOKEN)

# https://discordapp.com/oauth2/authorize?client_id=688534221324943360&scope=bot&permissions=8