import os
import re
from twitchio.ext import commands

# set up the bot
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=os.environ['CHANNEL'].split(',')
)

timecode = ""

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    #ws = bot.ws  # this is only needed to send messages within event_ready
    #await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")
    # await ctx.channel.send(f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, {ctx.author.name}!")


@bot.command(name='test')
async def test1(ctx):
    print(ctx.content)
    print(ctx.channel)
    for i in dir(ctx):
        print(getattr(ctx,i))

    await ctx.send('test passed! message:'+ctx.content[6:])

@bot.command(name='clip')
async def startClip(ctx):
    inputTimeCode =
    print(ctx.channel+" start cliping at "+ctx.content[6:]);

    await ctx.send('')

def timeCodeTest(timecode):
    pattern = r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    if re.fullmatch(pattern, timecode):
        print("re pass")
        return True
    else:
        print("re fail")
        return False


if __name__ == "__main__":
    print(f"Bots try to go into {os.environ['CHANNEL']} chatroom...")
    timeCodeTest("11:00:11")
    timeCodeTest("a")
    #bot.run()
