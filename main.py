import asyncio
import logging
import os

import discord
from discord import File
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace this with your Discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = str(os.getenv('CHANNEL_ID'))  # Replace with the ID of the channel you want to upload files to

# Create a new Discord client with the required intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent if needed
client = discord.Client(intents=intents)

# Define a FileSystemEventHandler to handle file events
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory:
            # Get the file path
            file_path = event.src_path
            logging.debug(f"File created: {file_path}")

            # Check if the file is output.webm
            if file_path.endswith("output.webm"):
                logging.info(f"Detected new file: {file_path}")
                # Handle the file upload asynchronously
                self.loop.create_task(handle_file_upload(file_path))
            else:
                logging.debug(f"Skipping file: {file_path}")

async def handle_file_upload(file_path):
    # Upload the file to the Discord channel
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        logging.error(f"Failed to get channel with ID {CHANNEL_ID}")
        return

    with open(file_path, 'rb') as f:
        file = File(f)
        try:
            response = await channel.send(file=file)
            logging.debug(f"Uploaded file: {file_path} - Response: {response}")
        except discord.errors.HTTPException as e:
            logging.error(f"Failed to upload file: {file_path} - {e.response.status} - {e.text}")
        except Exception as e:
            logging.error(f"Unexpected error while uploading file: {file_path} - {e}")

# Set up the file observer
observer = Observer()
folder_to_watch = os.getenv('FOLDER_TO_WATCH')

async def main():
    loop = asyncio.get_event_loop()
    event_handler = FileEventHandler(loop)
    observer.schedule(event_handler, folder_to_watch, recursive=True)

    # Start the Discord client and the file observer
    @client.event
    async def on_ready():
        logging.info(f"Logged in as {client.user}")
        observer.start()
        logging.info("File observer started")

        try:
            while True:
                await asyncio.sleep(1)  # Add a small delay to avoid blocking the event loop
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            logging.info("File observer stopped")

    await client.start(TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
