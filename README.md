Discord File Upload Bot

This bot automatically uploads files named output.webm from a specified folder to a designated Discord channel.
Setup

- Install Python on your machine.
- Clone or download this repository.
- Configure the bot with your Discord bot token and the channel ID where you want files uploaded.
- Set the folder path that the bot should monitor for new output.webm files.
- Run the bot script.

Once running, the bot will continuously watch the specified folder. Whenever a new output.webm file is created, it will
automatically upload the file to the designated Discord channel.

This bot utilizes the discord.py library and the watchdog library for monitoring file system events. It is designed for
ease of use, automating the process of sharing specific files on Discord.

For detailed instructions and configuration options, please refer to the documentation within the repository.