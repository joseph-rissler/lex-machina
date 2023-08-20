import logging
import asyncio
import math

from typing import Optional

import discord

import config
import rules
from data import data


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Client(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tree = discord.app_commands.CommandTree(self)
    
    async def setup_hook(self):
        self.add_view(ProposalView())
        self.tree.copy_global_to(guild=config.guild)
        await self.tree.sync(guild=config.guild)
    
    def command(self, func):
        return self.tree.command()(func)

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents = intents)

@client.event
async def on_message(message):
    if message.channel.id == config.channel.id and not message.author.bot:
        await rules.on_message(message)

async def proposal_update(self, message):
    proposal = data.proposals[message.id]
    check_response = rules.check_proposal(proposal)
    if check_response:
            await message.edit(view=None)
            await message.reply(check_response)
            del data.proposals[message]
    

class ProposalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green, emoji="👍", custom_id="support")
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        data.proposals[interaction.message].votes[interaction.user.id] = 1
        await proposal_update(interaction, interaction.message)
        await interaction.response.send_message("Support Recorded", ephemeral=True)
        
    @discord.ui.button(style=discord.ButtonStyle.red, emoji="👎", custom_id="oppose")
    async def oppose(self, interaction: discord.Interaction, button: discord.ui.Button):
        data.proposals[interaction.message].votes[interaction.user.id] = -1
        await proposal_update(interaction, interaction.message)
        await interaction.response.send_message("Opposal Recorded", ephemeral=True)

@client.command
async def propose(interaction: discord.Interaction, proposal_text: str):
    await interaction.response.send_message(proposal_text, view=ProposalView())
    message = await interaction.original_response()

@client.command
async def set_points(interaction: discord.Interaction, member: discord.Member, points: int):
    if interaction.user.id == config.gamemaster.id:
        data.players[member].points = points
        await interaction.response.send_message(f'{member.mention}, you have {points} points')
        data.save()
    else:
        await interaction.response.send_message('no', ephemeral=True)

@client.command
async def points(interaction: discord.Interaction, member: Optional[discord.Member]):
    if member is None:
        member = interaction.user
    if member.bot:
        msg = f'{member.mention} has {math.pi} points.'
    else:
        points = data.players[member].points
        if member.id == interaction.user.id:
            msg = f'You have {points} points.'
        else:
            msg = f'{member.mention} has {points} points.'
    await interaction.response.send_message(msg, ephemeral=True)

#if TESTING:
#    import code
#    code.InteractiveConsole(locals=globals()).interact()
#else:
client.run(config.token)

