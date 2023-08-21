import sys
import discord
from types import SimpleNamespace

config = SimpleNamespace()

def init_config(mode=None):
    
    config.gamemaster = discord.Object(id=373840269050642442) #undecim11

    if mode == 'test':
        config.tokenfile = "TOKEN.testing"
        config.datafile = "testing.pickle"
        config.channel = discord.Object(id=1141553139779125258)
        config.guild = discord.Object(id=436960665647972368)
        config.point_emoji = "👁️"
    else:
        config.tokenfile = "TOKEN"
        config.datafile = "data.pickle"
        config.channel = discord.Object(id=1135339346443124817)
        config.guild = discord.Object(id=1135339345990135880)
        config.point_emoji = discord.PartialEmoji(name='point', id=1137681095614275646)

    with open(config.tokenfile) as f: config.token = f.read().strip()
