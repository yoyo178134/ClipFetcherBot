import os
import re
import json
from datetime import datetime
from twitchio.ext import commands

# set up the bot 6
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    # initial_channels=os.environ['CHANNEL']
    initial_channels=os.environ['CHANNEL'].split(',')
)

usingClip = dict()
createTime = dict()

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    #ws = bot.ws  # this is only needed to send messages within event_ready
    #await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")
    #await ctx.channel.send(f"/me has landed!")


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
    print((ctx.message.timestamp))
    await ctx.send('/me test passed! message:' + ctx.content[6:])


@bot.command(name='botclear')
async def botclear(ctx):
    print(ctx.channel.name + "'using dict is clear")
    if ctx.channel.name in usingClip:
        del usingClip[ctx.channel.name]
    await ctx.send('/me dict clear done! ')


def timeCodeTest(timecode):
    pattern = r"[+-][0-9]{2,}"  # +121 or -12
    patternTime = r"\d{2,}:\d{2}:\d{2}"     # %H:%M:%S
    if re.fullmatch(pattern, timecode):
        print(timecode+" pass")
        return True
    elif timecode =='' :
        print(timecode + " pass")
        return True
    elif re.fullmatch(patternTime, timecode):
        print(timecode+" pass")
        return True
    else:
        print(timecode + " fail")
        return False

@bot.command(name='uptime')
async def uptime(ctx):
    re = await ctx.channel.get_stream()
    if re:

        stamp = datetime.fromisoformat(re['started_at'][:-1])
        stamp =   datetime.utcnow() - stamp
        hour = str(int(stamp.total_seconds()//3600))
        min = str(int((stamp.total_seconds()%3600) // 60))
        sec = str(int((stamp.total_seconds()%3600) % 60))
        await ctx.send('/me Has been Streaming for '+hour+':'+min+":"+sec) #timedelta to %H:%M:%S
        return  stamp
    else:
        await ctx.send('/me Not Streaming  ')
        return None

@bot.command(name='createtime')
async def createtime(ctx):
    re = await ctx.channel.get_stream()
    if re:
        stamp = datetime.fromisoformat(re['started_at'][:-1])
        await ctx.send('/me ' + stamp.strftime("%m/%d/%Y, %H:%M:%S"))
        return stamp
    else:
        await ctx.send('/me Not Streaming  ')
        return None

@bot.command(name='mytime')
async def mytime(ctx):
    await ctx.send('/me '+(ctx.message.timestamp).strftime("%m/%d/%Y, %H:%M:%S"))
    return ctx.message.timestamp


@bot.command(name='startclip')
async def startClip(ctx):
    inputTimeCode = ctx.content[11:]
    if timeCodeTest(inputTimeCode):
        print(ctx.channel.name + " start cliping  " + inputTimeCode + " by " + ctx.author.name)
        if ctx.author.name in usingClip[ctx.channel.name]:
            print(usingClip)
            await ctx.send('/me @' + ctx.author.name + ' Clip start fail! Please use !endclip or !botclear')
            return
        else:
            usingClip[ctx.channel.name].append(ctx.author.name)
            print("push " + ctx.author.name)
            await ctx.send('/me @' + ctx.author.name + ' Clip start success ' + inputTimeCode)
            return
    #else:
        #await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')


@bot.command(name='endclip')
async def endClip(ctx):
    inputTimeCode = ctx.content[9:]
    if timeCodeTest(inputTimeCode):
        if ctx.author.name in usingClip[ctx.channel.name]:
            usingClip[ctx.channel.name].remove(ctx.author.name)
            print("pop "+ctx.author.name)
            await ctx.send('/me @' + ctx.author.name + ' Clip end success ' + inputTimeCode)
            return
        else:
            print(usingClip)
            await ctx.send('/me @' + ctx.author.name + ' Clip end fail! Please use !startclip')
            return
        # print(ctx.channel.name + " start cliping at " +inputTimeCode+" by "+ctx.author.name)
    #else:
        #await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')



@bot.command(name='createclip')
async def createclip(ctx):
    inputTimeCode = ctx.content[12:]
    if timeCodeTest(inputTimeCode):
        await ctx.send('/me @' + ctx.author.name + ' Clip created success ' + inputTimeCode)
        # print(ctx.channel.name + " start cliping at " +inputTimeCode+" by "+ctx.author.name)
    else:
        await ctx.send('/me Invalid input! Time code format: +xxx or -xxx')



if __name__ == "__main__":
    print(f"Bots try to go into {os.environ['CHANNEL']} chatroom...")
    for i in os.environ['CHANNEL'].split(','):
        usingClip[i] = list()
    bot.run()

    #asyncio.run(bot.start())
