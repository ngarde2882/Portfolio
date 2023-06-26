import nextcord.ui
from nextcord.ext import commands
from RoleView import RoleView
from config import BOT_TOKEN, GUILD_ID, THE_GOOBER

command_prefix = "!"
class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_connect(self):
        print("Connected!")

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(RoleView())
            self.persistent_views_added = True
        print(f"Logged in as {self.user}")

intents = nextcord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=command_prefix, intents=intents)

@bot.command()
async def goober(ctx: nextcord.ext.commands.Context):
    print("goober ran")
    if ctx.message.author.id == THE_GOOBER:
        view5 = RoleView()
        await ctx.send("PRESS THE BUTTON, STANLEY", view=view5)

bot.run(BOT_TOKEN)