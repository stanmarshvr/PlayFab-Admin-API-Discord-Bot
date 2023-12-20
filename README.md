# PlayFab-Admin-API-Discord-Bot
This is a pretty simple Discord bot written in Python that has commands that make API requests to your PlayFab title to do things like ban players, give items, give virtual currency, delete players, etc. Feel free to skid this, just give credits please.
# Commands:
```
  So Far you can do some slash commands
  do /help
  /ban
  /delete_player (NOT TESTED)
```
# Installing and Configuration:
1. Install Python (https://www.python.org)
2. Download the code as a zip file, or git clone the repository
3. Run install.bat to install the dependencies (discord.py and requests)
4. Obviously if you havent already, create your PlayFab title (https://developer.playfab.com) and get the title ID and secret key, and create your Discord bot (https://discord.com/developers) and get the token
5. Open config.json and change the values to your PlayFab info and discord info in their respective places, also you can change the command prefix.
Done!

# Using the bot:
Simply add your created Discord bot to the server you want, then run start.bat and then people that have the role you specified in config.json can run the commands! Have fun!


# Extra:
Change Around some of the settings like the embed stuff saying JTMC's bot.
