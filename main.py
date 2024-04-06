# Packages

from datetime import datetime

import discord
from discord import app_commands

# Setup

channel_logs = {}

with open('token.txt', 'r') as file:
    token = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Local functions

def get_timestamp():
    return f'[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}]'

def convert_emoji(emoji: str):
    return emoji.encode('unicode-escape')
def convert_raw_str(s: str):
    return repr(s)[1:-1]

def join_escape(t: any):
    return '\n'.join(t)

def format_user_str(user: discord.Member | discord.User):
    # TODO: Clean up
    if user.bot:
        return f'Bot {user.display_name} (@{user.name}, <@{user.id}>)'
    else:
        return f'User {user.display_name} (@{user.name}, <@{user.id}>)'
def format_message_str(message: discord.Message):
    # TODO: Clean up
    if message.reference:
        if message.attachments:
            attachment_ids = []
            
            for attachment in message.attachments:
                attachment_ids.append(f'<{attachment.id}>')
            
            if message.content:
                return f'message \'{convert_raw_str(message.content)}\' (id <{message.id}>) replying to message <{message.reference.message_id}> with attachment(s) {', '.join(attachment_ids)}'
            else:
                return f'empty message (id <{message.id}>) replying to message <{message.reference.message_id}> with attachment(s) {', '.join(attachment_ids)}'
        else:
            if message.content:
                return f'message \'{convert_raw_str(message.content)}\' (id <{message.id}>) replying to message <{message.reference.message_id}>'
            else:
                return f'empty message (id <{message.id}>) replying to message <{message.reference.message_id}>'
    else:
        if message.attachments:
            attachment_ids = []
            
            for attachment in message.attachments:
                attachment_ids.append(f'<{attachment.id}>')
            
            if message.content:
                return f'message \'{convert_raw_str(message.content)}\' (id <{message.id}>) with attachment(s) {', '.join(attachment_ids)}'
            else:
                return f'empty message (id <{message.id}>) with attachment(s) {', '.join(attachment_ids)}'
        else:
            if message.content:
                return f'message \'{convert_raw_str(message.content)}\' (id <{message.id}>)'
            else:
                return f'empty message (id <{message.id}>)'

# Client events

@client.event
async def on_ready():
    print('Online')

    await tree.sync()
    print('Command tree synced')

    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name='channel activity', type=discord.ActivityType.listening))
    print('Presence updated')

    print('Ready')
@client.event
async def on_typing(channel, user, when):
    if channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(user)} started typing'
        
        channel_logs[channel.id].append(log_string)
@client.event
async def on_message(message):
    if message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(message.author)} sent {format_message_str(message)}'
        
        channel_logs[message.channel.id].append(log_string)
@client.event
async def on_message_edit(before, after):
    if after.channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(after.author)} edited {format_message_str(before)} to {format_message_str(after)}'
        
        channel_logs[after.channel.id].append(log_string)
@client.event
async def on_message_delete(message):
    if message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(message.author)} deleted {format_message_str(message)}'
        
        channel_logs[message.channel.id].append(log_string)
@client.event
async def on_bulk_message_delete(messages):
    timestamp = get_timestamp() # Retrieve timestamp now for maximum time accuracy (below algorithm may take a few milliseconds to compute)
    
    message_channels = {}
    
    for message in messages:
        if not message.channel.id in message_channels:
            message_channels[message.channel.id] = []
        
        message_channels[message.channel.id].append(message)

    for channel_id in message_channels:
        if channel_id in channel_logs:
            log_string = f'[{timestamp}] The following messages were bulk-deleted: \'{join_escape(channel_logs[channel_id])}\''

            channel_logs[channel_id].append(log_string)
@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(user)} added reaction \'{convert_emoji(str(reaction))}\' to {format_message_str(reaction.message)}'
        
        channel_logs[reaction.message.channel.id].append(log_string)
@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} {format_user_str(user)} removed reaction \'{convert_emoji(str(reaction))}\' from {format_message_str(reaction.message)}'
        
        channel_logs[reaction.message.channel.id].append(log_string)
@client.event
async def on_reaction_clear(message, reactions):
    if message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} Reactions cleared on message {format_message_str(message)}'

        channel_logs[message.channel.id].append(log_string)
@client.event
async def on_reaction_clear_emoji(reaction):
    if reaction.message.channel.id in channel_logs:
        log_string = f'{get_timestamp()} All {convert_emoji(str(reaction))} reactions removed from {format_message_str(reaction.message)}'

        channel_logs[reaction.message.channel.id].append(log_string)
@client.event
async def on_guild_channel_delete(channel):
    # TODO: Send logs to different channel..?
    if channel.id in channel_logs:
        channel_logs.pop(channel.id)

# Commands

@tree.command(name='start', description='Start recording this channel')
async def _start(interaction):
    if interaction.channel_id in channel_logs:
        await interaction.response.send_message('This channel is already being recorded. Execute __/stop__ to stop recording.')
    else:
        await interaction.response.send_message('This channel is now being recorded. Execute __/stop__ to stop recording.')

        channel_logs[interaction.channel_id] = [f'{get_timestamp()} -- RECORDING START --']
@tree.command(name='stop', description='Stop recording this channel')
async def _stop(interaction):
    if interaction.channel_id in channel_logs:
        channel_logs[interaction.channel_id].append(f'{get_timestamp()} -- RECORDING END --')
        
        with open(f'logs/{interaction.channel_id}.txt', 'w') as log_file:
            log_file.write(join_escape(channel_logs[interaction.channel_id]))
            
        await interaction.response.send_message(f'This channel has stopped being recorded. Execute __/start__ to start recording again.\n\nThe message log has been attached to this message as a `.txt` file.', file=discord.File(f'logs/{interaction.channel_id}.txt', filename='log.txt', spoiler=False))
        
        channel_logs.pop(interaction.channel_id)
    else:
        await interaction.response.send_message('This channel is not currently being recorded. Execute __/start__ to start recording.')
@tree.command(name='help', description='Get help about operating this bot')
async def _help(interaction):
    await interaction.response.send_message(
        """
        """)

# Run client with token

client.run(token)
