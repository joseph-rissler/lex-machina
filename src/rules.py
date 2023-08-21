import re
import discord
from data import data

from config import config

async def on_message(message):
    if message_can_score(message):
        player = data.players[message.author]
        player.points += 1
        player.last_score_date = message.created_at.date()
        data.save()
        await message.add_reaction(config.point_emoji)

def check_proposal(proposal):
    total = data.players.total_points
    uncounted = total - proposal.counted
    score = proposal.score
    lowest = score - uncounted
    highest = score + uncounted
    threshold = (total * 2) // 3
    if lowest > threshold:
        return "Proposal PASSED!"
    elif highest <= threshold:
        return "Proposal REJECTED!"

def message_can_score(message):
    return check_message_date(message) \
       and doesnt_start_with_vowel(message.content) \
       and contains_acronym(message.content) \
       and ends_with_new_score(message)

def check_message_date(message):
    return data.players[message.author].last_score_date != message.created_at.date()

def doesnt_start_with_vowel(text):
    return text[0].lower() not in 'aeiou'

'''
Compile the list of acronyms for regex matching. Colon (:) represents optional
"soft breaks" so that e.g "WTF" is equivalent to e.g. "w.t.f."
Period (.) and slash (/) are converted to colon before matching the text.
'''
with open('acronyms') as file_:
    acronyms = list()
    for line in file_:
        line = line.strip().casefold() 
        if len(line) < 1: continue # might be blank lines
        acronyms.append(re.compile(r'\b' + ':?'.join(line) + r'\b'))

def contains_acronym(text):
    text = text.casefold().replace('.',':').replace('/', ':')
    for acronym in acronyms:
        if acronym.search(text):
            return True

def ends_with_new_score(message):
    regex = r'((?<=score)|(?=.*?\d+.*?points))(.*?(?P<new_score>\d+))' #This one was fun.
    if match := re.search(regex,message.content.lower()):
        current_score = data.players[message.author].points
        if int(match['new_score']) == current_score + 1:
            return True




