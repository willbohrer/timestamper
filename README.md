# Timestamper v1.0.0

## About

Discord bot that precisely records activity in channels down to the microsecond and logs it for you.

Written in Python 3.12.2 and utilizes [discord.py 2.3.2](https://github.com/Rapptz/discord.py).

## Installation

To install Python, follow the instructions on [its dedicated website](https://www.python.org). The latest version is preferable. Anything at or above 3.12.2 should definitely work.
To install discord.py, follow the instructions on [its repository](https://github.com/Rapptz/discord.py). The latest version is preferable. Anything at or above 2.3.2 should definitely work.

To install the bot, simply download the source code as a .zip and extract it to a folder of your choice on your computer. Assuming you have already created an application in the [Discord developer portal](https://discord.com/developers/applications), copy its token and paste it into the `token.txt` file in the folder. Just run `main.py` and the bot will run.

**If you are unable or don't want to host yourself, an alternative is adding the [official Timestamper bot](https://discord.com/oauth2/authorize?client_id=1225659795558895626) to your server.**

## Debugging

Most problems root from your bot's intents being disabled. Try enabling all three gateway intents for your bot in the developer portal.

![image](https://github.com/willbohrer/timestamper/assets/150475693/2ef29504-d1a3-4374-9a17-8717a92e40f7)

Other problems could be the bot not having the correct permissions in servers. Make sure that `applications.commands`, `bot`, and `Administrator` permissions are all enabled.

![image](https://github.com/willbohrer/timestamper/assets/150475693/85b53c71-e879-44b1-b822-aece46dec1fe)

Otherwise, create an issue.
