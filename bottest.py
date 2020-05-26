from twitchio.ext import commands




class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:48g0yxyc9xk1wcwvc2i3pdmikmc4wx',
    client_id='dxuxin2d8vjx0ylzx5wdxr2k0n6gqu',
    nick='clipBOT',
    prefix='!',
    initial_channels=['yoyo178'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        print(f'Ready | {self.channel}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await self.get_stream(self.channel) and await self.get_chatters(channel=self.channel)



bot = Bot()
bot.run()
