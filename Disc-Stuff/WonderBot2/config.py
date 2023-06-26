from dotenv.main import load_dotenv
import os
load_dotenv()
GUILD_ID = int(os.getenv("DISCORD_GUILD",""))
BOT_TOKEN = os.getenv("DISCORD_TOKEN","")
BOT_NAME = "WonderBot2"
GOOBER_ID = int(os.getenv("GOOBER_ID",""))
THE_GOOBER = int(os.getenv("THE_GOOBER",""))