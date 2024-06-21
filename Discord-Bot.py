import os
from typing import Final
import discord
from discord import Intents,Client,Message,app_commands
from dotenv import load_dotenv
from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    wis = ['wisdom','Wisdom','Tell','tell','pour','Pour','some','Some','more']
    if 'how are you' in lowered:
       return 'well , you are so silent today'
    elif 'bye' in lowered:
       return 'see youuu!!!!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    elif 'real' in lowered:
        return '"yesterday is history, tomorrow is a mistery, but today is a gift. Thats why its called The Present."'
    elif any(word in lowered for word in wis):
        return choice([
           '"What a good day "',
           '"how about we go out for dinner"',
           '"Veera Ragahavan is the greatest young skipper to ver go down in history"',
           '"It is tomorrow by together then"',
           '"How about we buy a home in japan"'
        ])
    else:
        return choice([
            'I do not understand sorry',
                'what are you talking about?',
                'do you mind rephrasing it?'

        ])
    
#loading token
 #   Token: Final[str] = os.getenv('Token')
 #   print(Token)

#bot setup
#intents are permission for the bot to view the messages
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)
#message functions
async def send_message(message: Message, user_message: str) -> None:
    if not user_message: 
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?': #private messaging
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response+"- The cherry master")  if is_private else await message.channel.send(response+" - The cherry master") 
    except Exception as e:
        print(e)

#bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


#handling reply and messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: #checks if the user msges
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

@tree.command(name="master")
async def master(interaction: discord.integrations):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!")

#main 
def main() -> None:
    client.run('token')

if __name__ == '__main__':
    main()