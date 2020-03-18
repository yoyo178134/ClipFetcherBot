from twitchio.ext import commands


bot = commands.Bot(
    # set up the bot
    irc_token='oauth:48g0yxyc9xk1wcwvc2i3pdmikmc4wx',
    client_id='dxuxin2d8vjx0ylzx5wdxr2k0n6gqu',
    nick='clipBOT',
    prefix='!',
    initial_channels=['yoyo87870521']
)
bot.run()