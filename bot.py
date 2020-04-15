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

usingClip = {}


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    # ws = bot.ws  # this is only needed to send messages within event_ready
    # await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")
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
    '''
    print(ctx.content)
    print(ctx.channel)
    for i in dir(ctx):
        print(getattr(ctx, i))
    '''
    print(usingClip.items())
    await ctx.send('/me test passed! message:' + ctx.content[6:])


@bot.command(name='botclear')
async def botclear(ctx):
    print(ctx.channel.name + "'using dict is clear")
    if ctx.channel.name in usingClip:
        del usingClip[ctx.channel.name]
    await ctx.send('/me dict clear done! ')


def timeCodeTest(timecode):
    pattern = r"[+-][0-9][0-9][0-9]"  # +121 or -12
    if re.fullmatch(pattern, timecode):
        return True
    else:
        return False


@bot.command(name='startclip')
async def startClip(ctx):
    inputTimeCode = ctx.content[11:]
    if timeCodeTest(inputTimeCode):
        print(ctx.channel.name + " start cliping at " + inputTimeCode + " by " + ctx.author.name)
        if ctx.author.name in usingClip[ctx.channel.name]:
            await ctx.send('/me @' + ctx.author.name + 'Clip start fail! Please use !endclip or !botclear')
        else:
            usingClip[ctx.channel.name] = ctx.author.name
            await ctx.send('/me @' + ctx.author.name + 'Clip start success at ' + inputTimeCode)

    else:
        await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')


@bot.command(name='endclip')
async def endClip(ctx):
    inputTimeCode = ctx.content[9:]
    if timeCodeTest(inputTimeCode):
        if ctx.author.name in usingClip[ctx.channel.name]:
            usingClip[ctx.channel.name] = ctx.author.name
            await ctx.send('/me @' + ctx.author.name + 'Clip end success at ' + inputTimeCode)

        else:
            await ctx.send('/me @' + ctx.author.name + 'Clip end fail! Please use !startclip')
        # print(ctx.channel.name + " start cliping at " +inputTimeCode+" by "+ctx.author.name)
    else:
        await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')



@bot.command(name='createclip')
async def createclip(ctx):
    inputTimeCode = ctx.content[12:]
    if timeCodeTest(inputTimeCode):
        await ctx.send('/me @' + ctx.author.name + 'Clip created success at ' + inputTimeCode)
        # print(ctx.channel.name + " start cliping at " +inputTimeCode+" by "+ctx.author.name)
    else:
        await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')

'''
@bot.command(name='clip')
async def startClip(ctx):
    inputTimeCode = ctx.content[6:]
    if(timeCodeTest(inputTimeCode)):
        await ctx.send('/me Clip start at ' +inputTimeCode)
        print(ctx.channel.name + " start cliping at " +inputTimeCode)
    else:
        await ctx.send('/me Invalid input! Time code format:xx:xx:xx')



    await ctx.send('')

def timeCodeTest(timecode):
    pattern = r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    if re.fullmatch(pattern, timecode):
        print("re pass")
        return True
    else:
        print("re fail")
        return False
'''

if __name__ == "__main__":
    print(f"Bots try to go into {os.environ['CHANNEL']} chatroom...")
    for i in os.environ['CHANNEL'].split(','):
        usingClip[i] = list()
    bot.run()
