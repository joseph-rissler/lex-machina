import sys
import discord

testing = (len(sys.argv) > 1 and sys.argv[1] == 'test')

gamemaster = discord.Object(id=373840269050642442) #undecim11

if testing:
    tokenfile = "TOKEN.testing"
    datafile = "testing.pickle"
    channel = discord.Object(id=1141553139779125258)
    guild = discord.Object(id=436960665647972368)
    point_emoji = "👁️"
else:
    tokenfile = "TOKEN"
    datafile = "data.pickle"
    channel = discord.Object(id=1135339346443124817)
    guild = discord.Object(id=1135339345990135880)
    point_emoji = discord.PartialEmoji(name='point', id=1137681095614275646)

with open(tokenfile) as f: token = f.read().strip()
