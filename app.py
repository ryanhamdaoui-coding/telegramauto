from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
from telethon import TelegramClient, events
import asyncio
import logging
import os

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
API_ID = int(os.getenv("TELEGRAM_API_ID"))  # Convert to integer
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER")
BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")  # Bot username

# Initialize the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)


async def interact_with_bot():
    try:
        # Start the Telegram client
        await client.start(PHONE_NUMBER)
        logger.info("Logged into Telegram!")

        # Start a conversation with the bot
        async with client.conversation(BOT_USERNAME) as conv:
            # Send a message to the bot
            await conv.send_message("0562407034")
            logger.info("Message sent to bot.")

            # Wait for the bot's response
            response = await conv.get_response()
            logger.info(f"Bot responded: {response.text}")

            # Click the last button (if available)
            if response.buttons:
                # Get the last button in the last row
                last_button = response.buttons[-1][-1]
                await last_button.click()
                logger.info("Clicked the last button.")
            else:
                logger.info("No buttons found in the response.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


# Schedule the task to repeat every 12 hours
async def schedule_task():
    while True:
        await interact_with_bot()
        logger.info("Task complete. Waiting for 12 hours...")
        await asyncio.sleep(12 * 60 * 60)  # Wait 12 hours


# Run the task
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule_task())
