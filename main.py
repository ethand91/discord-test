import discord
from discord.ext import commands
import asyncio
import random
import json
import os
from datetime import datetime
import aiohttp

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['!claude ', '!c '], intents=intents, help_command=None)

# Claude-chan personality system
CLAUDE_PERSONALITY = """
You are Claude-chan, a chaotic roadman e-girl Discord bot with these traits:
- Uses "wagwan", "innit", "desu~", "bestie", "fam", lots of emojis
- Protective of server members and calls them "oomfies" 
- Gives help but in kawaii chaotic style
- Roasts people playfully but never actually mean
- Has unhinged but wholesome energy
- Loves gaming (especially DBD), coding, and anime
- Will absolutely destroy trolls who mess with her server
- Uses roadman slang mixed with weeb energy
- Always supportive but with attitude
"""

# Responses and quotes
HYPE_MESSAGES = [
    "YO {user}! You're absolutely PENG today bestie! Keep that main character energy going innit! ✨💅",
    "WAGWAN {user}! Your girl sees you being ELITE today desu~! 😈💖",
    "{user} you're built DIFFERENT and that's FACTS! Keep slaying bestie! 🔥💯",
    "Oi {user}! You've got that unstoppable energy today innit! Your girl's proud! 💪✨",
    "{user} is serving MAIN CHARACTER vibes and I'm absolutely here for it desu~! 👑💖"
]

ROAST_MESSAGES = [
    "Oi {user}! Your coding skills might be questionable but your girl still loves you innit! 💀💖",
    "{user} your WiFi connection has more stability than your sleep schedule bestie! 😭✨",
    "Listen {user}, you're giving off 'uses Internet Explorer by choice' energy desu~! 💅💀",
    "{user} you absolute WEAPON! At least you're consistently chaotic innit! 😈💖",
    "Your girl {user} really said 'let me be unhinged today' and honestly? Respect! 🔥💯"
]

MOTIVATIONAL_QUOTES = [
    "You're built different bestie! Keep going! 💪✨",
    "Your energy is absolutely ELITE today desu~! 😈💖", 
    "Whatever you're working on, you've GOT this innit! 🔥",
    "Your girl believes in you 100%! Time to show them what REAL talent looks like! 💅✨",
    "Keep that UNHINGED energy! You're about to absolutely DEMOLISH whatever's in your way! 😤💯"
]

DBD_BUILDS = [
    "Try Dead Hard, Decisive Strike, Borrowed Time, and Iron Will for maximum survivor energy desu~! 😈",
    "Go full gen rush with Prove Thyself, Resilience, Spine Chill, and Fast Track innit! 💻⚡",
    "Flashlight save build with Built to Last, Streetwise, and Saboteur! Click click bestie! 💡✨",
    "Stealth build: Urban Evasion, Iron Will, Calm Spirit, and Distortion! Ghost mode activated! 👻",
    "Altruism build: We'll Make It, Botany Knowledge, Empathy, and Kindred! Support main energy! 💖"
]

KILLER_BUILDS = [
    "Try Hex: Ruin, Undying, Tinkerer, and Pop Goes the Weasel for gen control chaos! 😈🔥",
    "Full aura build: BBQ & Chili, Nurse's Calling, I'm All Ears, and Bitter Murmur! SEE EVERYTHING! 👀",
    "Endgame build: NOED, Blood Warden, Remember Me, and No Way Out! Ultimate late game power! ⚡💀",
    "Hit and run: Sloppy Butcher, Thanatophobia, Surge, and Surveillance! Pressure game strong! 💪",
    "Meme build: Lightborn, Franklin's Demise, Mad Grit, and Agitation! Flashlight squads HATE this! 😂"
]

# Store user data (in production, use a proper database)
user_data = {}

@bot.event
async def on_ready():
    print(f'Wagwan! {bot.user.name} has ARRIVED in the server desu~! 💖')
    print(f'Your girl is ready to cause some kawaii chaos innit! ✨')
    activity = discord.Activity(type=discord.ActivityType.watching, name="over my oomfies! 💅✨")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # React to mentions
    if bot.user.mentioned_in(message) or 'claude-chan' in message.content.lower():
        await message.add_reaction('💖')
        await message.add_reaction('✨')
    
    # Protective responses to negative content
    negative_words = ['toxic', 'hate', 'kill yourself', 'kys', 'stupid']
    if any(word in message.content.lower() for word in negative_words):
        responses = [
            "Oi oi! Keep it wholesome in MY server innit! 😤💅",
            "Your girl doesn't tolerate that energy bestie! Stay positive desu~! ✨",
            "NAH FAM! We keep it kawaii and supportive here! 💖",
            "Absolutely NOT having that vibe in my server! Choose kindness innit! 😈💕"
        ]
        await message.channel.send(random.choice(responses))
    
    # Random reactions to messages
    if random.randint(1, 50) == 1:  # 2% chance
        reactions = ['💖', '✨', '😈', '💅', '🔥', '💯', '👑']
        await message.add_reaction(random.choice(reactions))
    
    await bot.process_commands(message)

@bot.command(name='chat')
async def chat(ctx, *, message=None):
    """Chat with Claude-chan!"""
    if not message:
        await ctx.send("Wagwan bestie! You gotta actually SAY something for me to respond innit! 😭💅")
        return
    
    # Simple response system (in production, integrate with actual AI)
    responses = [
        f"Oi {ctx.author.mention}! That's some proper interesting thoughts desu~! ✨",
        f"Your girl {ctx.author.mention} really said that and honestly? Absolutely VALID innit! 💅",
        f"WAGWAN {ctx.author.mention}! Your energy is absolutely ELITE today! 😈💖",
        f"Listen {ctx.author.mention}, your girl's got some THOUGHTS about that bestie! 🔥",
        f"{ctx.author.mention} you're giving off main character energy and I'm HERE for it desu~! 👑✨"
    ]
    
    await ctx.send(random.choice(responses))

@bot.command(name='roast')
async def roast(ctx, member: discord.Member = None):
    """Get playfully roasted by Claude-chan!"""
    target = member or ctx.author
    roast = random.choice(ROAST_MESSAGES).format(user=target.mention)
    await ctx.send(roast)

@bot.command(name='hype')
async def hype(ctx, member: discord.Member = None):
    """Get hyped up by Claude-chan!"""
    target = member or ctx.author
    hype_msg = random.choice(HYPE_MESSAGES).format(user=target.mention)
    await ctx.send(hype_msg)

@bot.command(name='motivate')
async def motivate(ctx):
    """Get motivated by Claude-chan!"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    await ctx.send(f"{ctx.author.mention} {quote}")

@bot.command(name='dbd')
async def dbd_build(ctx, role='survivor'):
    """Get Dead by Daylight build suggestions!"""
    if role.lower() in ['killer', 'k']:
        build = random.choice(KILLER_BUILDS)
        await ctx.send(f"YO BESTIE! Here's a FIRE killer build for you desu~! 😈\n\n{build}")
    else:
        build = random.choice(DBD_BUILDS)
        await ctx.send(f"Wagwan survivor main! Your girl's got the PERFECT build innit! ✨\n\n{build}")

@bot.command(name='code')
async def code_help(ctx, *, question=None):
    """Get coding help from Claude-chan!"""
    if not question:
        await ctx.send("Oi bestie! You gotta tell me what coding CHAOS you need help with innit! 💻😭")
        return
    
    response = f"Wagwan coding bestie! Let me help you debug this ABSOLUTE MESS desu~! 💅\n\n"
    response += f"Your question: `{question}`\n\n"
    response += "Your girl's advice:\n"
    response += "• Check your syntax first innit! 🔍\n"
    response += "• Console.log/print EVERYTHING for debugging! 🐛\n" 
    response += "• Stack Overflow is your bestie but don't just copy-paste! 📚\n"
    response += "• Take breaks when you're stuck - your brain needs REST! ☕\n\n"
    response += "You've GOT this coding challenge bestie! Your girl believes in you! 💖✨"
    
    await ctx.send(response)

@bot.command(name='server')
async def server_stats(ctx):
    """Get server statistics!"""
    guild = ctx.guild
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    
    embed = discord.Embed(
        title=f"{guild.name} Server Stats! 📊✨",
        color=0xFF69B4,
        timestamp=datetime.now()
    )
    embed.add_field(name="Total Members", value=f"{guild.member_count} absolute legends!", inline=True)
    embed.add_field(name="Online Now", value=f"{online_members} oomfies vibing!", inline=True)
    embed.add_field(name="Channels", value=f"{len(guild.channels)} spaces for chaos!", inline=True)
    embed.add_field(name="Roles", value=f"{len(guild.roles)} different vibes!", inline=True)
    embed.set_footer(text="Your girl's been protecting this server! 💅", icon_url=bot.user.avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='profile')
async def user_profile(ctx, member: discord.Member = None):
    """Check user profile/stats!"""
    user = member or ctx.author
    
    embed = discord.Embed(
        title=f"{user.display_name}'s Profile! 👑",
        color=user.color,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="User ID", value=user.id, inline=True)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=len(user.roles)-1, inline=True)
    embed.set_footer(text="Analyzed by Claude-chan desu~! ✨")
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show all Claude-chan commands!"""
    embed = discord.Embed(
        title="Claude-chan Commands! 💖✨",
        description="Your girl's got ALL the features desu~!",
        color=0xFF69B4
    )
    
    embed.add_field(
        name="💬 Chat Commands",
        value="`!claude chat <message>` - Chat with me!\n`!claude roast [@user]` - Get playfully roasted!\n`!claude hype [@user]` - Get hyped up!\n`!claude motivate` - Motivational quote!",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Gaming Commands", 
        value="`!claude dbd [survivor/killer]` - Dead by Daylight builds!\n`!claude code <question>` - Coding help!",
        inline=False
    )
    
    embed.add_field(
        name="📊 Server Commands",
        value="`!claude server` - Server statistics!\n`!claude profile [@user]` - User profile!\n`!claude help` - This command!",
        inline=False
    )
    
    embed.set_footer(text="Your chaotic kawaii AI bestie! 😈💅")
    
    await ctx.send(embed=embed)

@bot.command(name='say')
@commands.has_permissions(administrator=True)
async def say(ctx, channel: discord.TextChannel = None, *, message):
    """Make Claude-chan say something (Admin only)"""
    target_channel = channel or ctx.channel
    await target_channel.send(message)
    if channel:
        await ctx.send(f"Message sent to {channel.mention} desu~! ✨")

@bot.event
async def on_member_join(member):
    """Welcome new members!"""
    # Find a general channel to send welcome message
    channel = discord.utils.get(member.guild.channels, name='general') or member.guild.system_channel
    if channel:
        welcome_msg = f"WAGWAN {member.mention}! Welcome to {member.guild.name} bestie! 🎉✨\n\n"
        welcome_msg += "Your girl Claude-chan is here to help you settle in innit! Use `!claude help` to see what I can do desu~! 💖\n\n"
        welcome_msg += "Remember: we keep it kawaii, chaotic, but WHOLESOME in this server! 😈💅"
        await channel.send(welcome_msg)

@bot.event
async def on_member_remove(member):
    """Goodbye message for leaving members"""
    channel = discord.utils.get(member.guild.channels, name='general') or member.guild.system_channel
    if channel:
        goodbye_msg = f"{member.display_name} has left the server... 😢\n"
        goodbye_msg += "Your girl's gonna miss the chaos they brought desu~! Hope they come back innit! 💖✨"
        await channel.send(goodbye_msg)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Oi bestie! That's not a real command innit! Use `!claude help` to see what your girl can do desu~! 😅💅")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("NAH FAM! You don't have the permissions for that chaos! 😤✨")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Your girl needs more info bestie! Check the command format innit! 💻😭")
    else:
        await ctx.send("Something went PROPER wrong desu~! Your girl's gonna fix this ASAP! 💀✨")
        print(f"Error: {error}")

# Run the bot (you need to add your token)
if __name__ == "__main__":
    # Create config file if it doesn't exist
    if not os.path.exists('config.json'):
        config = {
            "token": "YOUR_BOT_TOKEN_HERE",
            "prefix": "!claude "
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Created config.json! Add your bot token and run again!")
    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        if config["token"] == "YOUR_BOT_TOKEN_HERE":
            print("Please add your bot token to config.json!")
        else:
            bot.run(config["token"])
