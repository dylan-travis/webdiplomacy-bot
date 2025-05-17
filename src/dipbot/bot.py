import discord
from discord.ext import commands
from dipbot.cogs import status
import os
import logging
from dipbot import app, scraper, utilities, bot_utilities
from dipbot.data_definitions import DipGame
import asyncio

COMMAND_PREFIX = "$"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('dipbot')

class DipBot(commands.Bot):
    def __init__(self):
        # Add intents parameter
        intents = discord.Intents.default()
        # Enable message content intent which is needed for command processing
        intents.message_content = True
        
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
    
    async def setup_hook(self):
        # This is called before the bot starts
        await self.add_cog(status.Status(self))

BOT = DipBot()

@BOT.event
async def on_ready():
    print("We have logged in as {0.user}".format(BOT))
    print(f"Use the command '{COMMAND_PREFIX}set_status_channel' in a channel to enable automatic status updates")

@BOT.event
async def on_message(message):
    # This is needed to process commands
    await BOT.process_commands(message)
    
    if bot_utilities.message_is_pleading_with_clientuserP(message, BOT.user):
        await message.channel.send(
            f"""I would love to help but I only understand a few messages, always prefixed by `{COMMAND_PREFIX}`. If you ask for `{COMMAND_PREFIX}help` I'll tell you about them."""
        )

def main():
    try:
        # Print environment variables for debugging
        print("Checking environment variables...")
        status_channel = os.environ.get("DIPBOT_STATUS_CHANNEL_ID")
        print(f"DIPBOT_STATUS_CHANNEL_ID = {status_channel}")
        game_id = os.environ.get("WEBDIP_GAME_ID")
        print(f"WEBDIP_GAME_ID = {game_id}")
        
        API_TOKEN = utilities.get_env_var_or_exit("DISCORD_API_KEY")
        print(f"Found Discord API key, starting bot...")
        # No need to add cog or listener here as they're handled in setup_hook and event decorators
        BOT.run(API_TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Make sure DISCORD_API_KEY is set in your environment variables.")
        print("You can set it with: export DISCORD_API_KEY='your_token_here'")
