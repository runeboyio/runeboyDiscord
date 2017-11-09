import discord
from discord.ext import commands
import logging
import asyncio
import re

description = "Runes Reforged Notation Discord Bot"

logging.basicConfig(level=logging.INFO)

#RUNE PATHING CONFIG
p = [
    ["Press the Attack","Lethal Tempo","Fleet Footwork"],
    ["Overheal", "Triumph","Presence of Mind"],
    ["Legend: Alacrity", "Legend: Tenacity", "Legend: Bloodline"],
    ["Coup De Grace", "Cut Down", "Last Stand"]
]
d = [
    ["Electrocute","Predator","Dark Harvest"],
    ["Cheap Shot", "Taste of Blood","Sudden Impact"],
    ["Zombie Ward", "Ghost Poro", "Eyeball Collection"],
    ["Ravenous Hunter", "Ingenious Hunter", "Relentless Hunter"]
]
s = [
    ["Summon Aery","Arcane Comet","Phase Rush"],
    ["Nullifying Orb", "Manaflow Band", "The Ultimate Hat"],
    ["Transcendence", "Celerity", "Absolute Focus"],
    ["Scorch", "Waterwalking", "Gathering Storm"]
]
r = [
    ["Grasp of the Undying", "Aftershock", "Guardian"],
    ["Unflinching", "Demolish","Font of Life"],
    ["Iron Skin", "Mirror Shell", "Conditioning"],
    ["Overgrowth", "Revitalize", "Second Wind"]
]
i = [
    ["Unsealed Spellbook","Glacial Augment","Kleptomancy"],
    ["Hextech Flashtraption", "Biscuit Delivery","Perfect Timing"],
    ["Magical Footwear", "Future's Market", "Minion Dematerializer"],
    ["Cosmic Insight", "Approach Velocity", "Celestial Body"]
]


#RUNE ORGANISING
def getRoute(c):
    return{
        'p': "Precision:",
        'd': "Domination:",
        's': "Sorcery:",
        'r': "Resolve:",
        'i': "Inspiration:",
    }[c]
 
 
def getRune(path, level, runeNum):
    level = int(level)
    runeNum = int(runeNum)
    return {
        'p': p[level][runeNum],
        'd': d[level][runeNum],
        's': s[level][runeNum],
        'r': r[level][runeNum],
        'i': i[level][runeNum],
    }[path]
 
 
def translateRune(r):
    path = getRoute(r[0])
    path = "**" + path + "**"
    runes = r[1:]
    for i in range(len(runes)):
        if(len(runes) == 3):
            if not runes[i] == '0':
                path += "\n>" + str(i+1) + ". " + getRune(r[0], i+1, int(runes[i])-1)
        else:
            path += "\n>" + str(i+1) + ". " + getRune(r[0], i, int(runes[i])-1)
    return path + "\n\n"
 
 
botCall = re.compile('\[\[\w*[:\s]+(?:(?:p|d|s|r|i)\s?(?:0|1|2|3){4}\s?(?:p|d|s|r|i)\s?(?:0|1|2|3){3})\]\]')
singleTree = re.compile('((?:p|d|s|r|i)(?:0|1|2|3){4})((?:p|d|s|r|i)\s?(?:0|1|2|3){3})')



#ACTUAL DISCORD SHIT
bot = commands.Bot(command_prefix="!", description=description)

@bot.event
async def on_ready():
	print("Logged in as",bot.user.name)


@bot.command(pass_context=True)
async def rune(ctx, champName: str, *, runesToCheck):
    splitRunes = runesToCheck.split(" ")
    firstFinishedRune = translateRune(splitRunes[0])
    secondFinishedRune = translateRune(splitRunes[1])
    combinedRunes = firstFinishedRune + secondFinishedRune
    splitRune2 = firstFinishedRune.split(".")
    name = splitRune2[1]
    name = name.replace("\n", "")
    name = name.strip(" ")
    name = name.replace(">2", "")
    if(champName == "gangplank") and (name == "Kleptomancy"):
        name = "bankplank"
        await bot.send_message(ctx.message.channel, "___***{0}***___\n{2}".format(name.upper(), champName.upper(), combinedRunes))
    else:
        await bot.send_message(ctx.message.channel, "___***{0} {1}***___\n{2}".format(name.upper(), champName.upper(), combinedRunes))

bot.run("token")
