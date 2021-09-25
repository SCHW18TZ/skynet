import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import asyncio
import psutil
import datetime
import utils

import base64
import io
# from discord_slash import SlashCommand
import random
from random import randint
from PIL import Image
from io import BytesIO
import praw
import pyfiglet
reddit = praw.Reddit(client_id='TstrVzGImmBtXg',
                     client_secret='erKyigzkq-v0MaN1SfFUwqW7o8CZFQ',
                     user_agent='Skynet')

# reddit = apraw.Reddit(username="",
#                       password="",
#                       client_id="",user_agent="apraw")										 
	
subreddit = reddit.subreddit("memes")

top = subreddit.top(limit=100) 

# for subbmission in top:
# print(subbmission.title)


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
#apraw sucks don't use this garbage!!!!!!!
    @commands.command()
    async def meme(self,ctx):
        subred = "memes"
        subreddit = reddit.subreddit(subred)
        all_subs = []
        top = subreddit.top(limit = 50)
    
        for subbmission in top:
            all_subs.append(subbmission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title= name)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command()
    async def security_help(self,ctx):
      await ctx.send("You can join our support server https://discord.gg/V8tu78KJbV or you can contact me or my marketing head bu typing .about")





   
    @commands.command(name="pog")
    async def pog(self, ctx):
        pog_gifs = [
            "https://tenor.com/view/pog-fish-fish-mouth-open-gif-17487624",
            "https://tenor.com/view/fish-pog-fish-poggers-fish-pog-champ-poggers-gif-16548474",
            "https://tenor.com/view/cat-happy-pog-cute-smile-gif-17223821",
            "https://tenor.com/view/vsauce-vsauce-pog-poggers-vsauce-poggers-pog-gif-18430372"
        ]

        await ctx.send(random.choice(pog_gifs))

    @commands.command(name="say")
    async def say(self, ctx, *, sentence: str):
        if len(ctx.message.mentions) + len(ctx.message.role_mentions) > 0:
            await ctx.send("You cannot mention people or roles using this command.")
            return

        if "@everyone" in ctx.message.content or "@here" in ctx.message.content:
            await ctx.send("You cannot mention people or roles using this command.")
            return
        await ctx.message.delete()
        await ctx.send(sentence)
# who is





    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content, member: discord.Member = None):
        if not member:  
            member = ctx.message.author
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                              title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f"Requested by {ctx.author}")
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime(
            "%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime(
            "%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

        embed.add_field(name="Roles:", value="".join(
            [role.mention for role in roles]), inline=False)
        embed.add_field(name="Highest Role:",
                        value=member.top_role.mention, inline=False)
        print(member.top_role.mention)
        await ctx.send(embed=embed)

    

    
    @commands.command(aliases=['hmm'])
    async def afk(self, ctx, member: discord.Member = None, *, reason=None):
      ctx.send(f"{ctx.author.mention} has gona afk {reason}")
    

    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")




    @commands.command(aliases=[ 'bet'])
    # @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


    @commands.command(aliases=['pl'])
    async def poll(self, ctx, *, msg):
        channel = ctx.channel
        try:
            op1, op2 = msg.split("or")
            txt = f"react with ✅ for {op1} or ❎ for {op2}"
        except:
            await channel.send("Correct syntax: 'Choice1' or 'Choice2' ")
            return

        embed = discord.Embed(title="Pool", description=txt,
                              colour=discord.Colour.blue())
        message_ = await channel.send(embed=embed)
        await message_.add_reaction("✅")
        await message_.add_reaction("❎")
        await ctx.message.delete()
		


    @commands.command()
    async def hack(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send('Put a member, dumbass')
        if member == ctx.author:
            await ctx.send('why would you hack yourself, idiot')
        if member != ctx.author:
            message = await ctx.send(f"Hacking {member.mention}")
            await asyncio.sleep(2)
            await message.edit(content="Logging their IP")
            await asyncio.sleep(3)
            await message.edit(content=f"{random.randint(10, 249)}.{random.randint(10, 249)}.{random.randint(10, 249)}.###")
            await asyncio.sleep(4)
            await message.edit(content="Stealing their Password")
            await asyncio.sleep(3)
            await message.edit(content=f"{member.name}IsCute{random.randint(0,999)}")
            await asyncio.sleep(4)
            await message.edit(content=f"Succesfully hacked {member.mention}, info is in database\nTotally legit hacking")

    @commands.command()
    async def vote(self, ctx, member: discord.Member = None):
      embed = discord.Embed(title = "Vote for skynet!",color = discord.Colour.green())
      embed.add_field(name = "<:vote:802026347731484682> now!",value = "[vote!](https://top.gg/bot/788612480636944414/vote)")
      embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author}")
      await ctx.send(embed=embed)  

    @commands.command()
    async def about(self, ctx, member: discord.Member = None):
      if not member:  # if member is no mentioned
          member = ctx.message.author  # set member as the author
      embed = discord.Embed(title = "Info",color = discord.Colour.green())
      embed.set_thumbnail(url = "https://imgur.com/a/ykYShXV")
      embed.add_field(name = "<a:redBadge:792301502474879016> official Website",value = "[Click here!](https://shitz.cf)",inline = False)
      embed.add_field(name = "<a:redBadge:792301502474879016> Support Sever!", value = "[click here!](https://discord.com/invite/V8tu78KJbV)",inline = False)
      embed.add_field(name = "Dev", value = "<a:redBadge:792301502474879016> SCHWITZ is the founder and creator of SkyNet is a game developer,a web developer and a discord bot developer making him a great full stack developer.His discord username is SCHWITZ#3875 <a:redBadge:792301502474879016>",inline = False)
      embed.add_field(name = "Marketing Head ", value = " <a:redBadge:792301502474879016> Deathsurfing more like suffering from succses is a full stack developer and marketing head of SkyNet.His discord username is 【𝔽𝕆】:sparkles:Death_Surfing#3093 <a:redBadge:792301502474879016>")
      embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author}")
      await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
      if not member:  # if member is no mentioned
          member = ctx.message.author  # set member as the author
      embed = discord.Embed(Title = f"{member.mention}'s avatar'",color = discord.Colour.purple())
      embed.set_image(url=member.avatar_url)
      embed.set_footer(icon_url=ctx.author.avatar_url,
                       text=f"Requested by {ctx.author}")
      embed.add_field(name="Display Name:", value=member.display_name)
      await ctx.send(embed = embed)

    # @commands.command()
    # async def say(self,ctx,*,msg):
    #   await ctx.message.delete()
    #   await ctx.send(msg)

    
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def dm(self, ctx, user_id: int, *, message: str):
        """ DM the user of your choice """
        user = self.bot.get_user(user_id)
        if not user:
            return await ctx.send(f"Could not find any UserID matching **{user_id}**")

        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user_id}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")

    @commands.command()
    async def wanted(self,ctx, user: discord.Member = None):
      if user == None:
          user = ctx.author

      wanted = Image.open('wanted.jpg')
      asset = user.avatar_url_as(size=128)
      data = BytesIO(await asset.read())
      php = Image.open(data)
      php = php.resize((244, 306))

      wanted.paste(php, (189, 262))

      wanted.save('profile.jpg')

      await ctx.send(file=discord.File('profile.jpg'))

    @commands.command()
    async def simp(self,ctx, user: discord.Member = None):
      if user == None:
          user = ctx.author

      wanted = Image.open('simo.jpg')
      asset = user.avatar_url_as(size=128)
      data = BytesIO(await asset.read())
      php = Image.open(data)
      php = php.resize((156, 277))

      wanted.paste(php, (93, 137))

      wanted.save('duh.jpg')

      await ctx.send(file=discord.File('duh.jpg'))




    @commands.command()
    async def slap(self,ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open('slap.jpg')
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        php = Image.open(data)
        php = php.resize((67, 58))

        wanted.paste(php, (108, 72))

        wanted.save('slapped.jpg')

        await ctx.send(file=discord.File('slapped.jpg'))

    @commands.command()
    async def delete(self,ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open('delete.jpg')
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        php = Image.open(data)
        php = php.resize((200, 200))

        wanted.paste(php, (117, 130))

        wanted.save('deleted.jpg')

        await ctx.send(file=discord.File('deleted.jpg'))




    @commands.command(name="8ball")
    @cooldown(1,5,BucketType.channel)

    async def eight_ball(self, ctx, *, question=None):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."
                     ]

        if question is not None:
            embed = discord.Embed(title=':8ball: 8ball', description=f'{ctx.author} asked a question.\n\nThe question was: {question}\n\n\n{random.choice(responses)}', colour=0x0000ff)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Ask me a question!')    
        

    @commands.command(name='ascii')
    async def ascii(self, ctx, *, msg: str):
        txt = pyfiglet.figlet_format(msg, font='big')
        await ctx.send(f"```{txt}```")

    @commands.command()
    async def roll(self,ctx):
      n = random.randrange(1,101)
      await ctx.send(n)

    @commands.command(aliases=['coin'])
    async def flipcoin(self, ctx):
        '''Flips a coin'''
        choices = ['You got Heads', 'You got Tails']
        color = discord.Color.green()
        em = discord.Embed(color=color, title='Coinflip:', description=random.choice(choices))
        await ctx.send(embed=em)


    @commands.command(aliases=['python', 'botinfo'])
    async def info(self, ctx):
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embedve = discord.Embed(
            title="Bot Info", description=None, color=0x9370DB)
        embedve.add_field(
            name="Bot Latency", value=f"Bot latency - {round(self.client.latency * 1000)}ms", inline=False)
        embedve.add_field(name='Hosting Stats', value=f'Cpu usage- {psutil.cpu_percent(1)}%'
                          f'\n(Actual Cpu Usage May Differ)'
                          f'\n'

                          f'\nNumber OF Cores - {psutil.cpu_count()} '
                          f'\nNumber of Physical Cores- {psutil.cpu_count(logical=False)}'
                          f'\n'

                          f'\nTotal ram- {round(values24, 2)} GB'
                          f'\nAvailable Ram - {round(val4, 2)} GB')

        await ctx.send(embed=embedve)

    @commands.command(name="reminder", aliases=["remind", "remindme", "remind_me", "rm"])
    async def reminder(self, ctx, time=None, *, reminder=None):
        embed = discord.Embed(color=self.theme_color,
                              timestamp=datetime.datetime.utcnow())
        seconds = 0
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        elif time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"

        if reminder is None:
            # Error message
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')

        if seconds == 0:
            embed.add_field(name='Warning', value='Please specify a proper duration.')

        if len(embed.fields) == 0:
            await ctx.send(f"Alright, I will remind you about **{reminder}** in **{counter}**.")
            await asyncio.sleep(seconds)
            await ctx.author.send(f"Hi, you asked me to remind you about **{reminder} {counter} ago**.")
            return

        await ctx.send(embed=embed)

    


    @commands.command(
        name='emojify', brief='Converts letters in a sentence to emojis',
        description='Converts letters in a sentence to emojis'
    )
    async def emojify(self, ctx, *, sentence):
        index = {
            'a': '🇦',
            'b': '🇧',
            'c': '🇨',
            'd': '🇩',
            'e': '🇪',
            'f': '🇫',
            'g': '🇬',
            'h': '🇭',
            'i': '🇮',
            'j': '🇯',
            'k': '🇰',
            'l': '🇱',
            'm': '🇲',
            'n': '🇳',
            'o': '🇴',
            'p': '🇵',
            'q': '🇶',
            'r': '🇷',
            's': '🇸',
            't': '🇹',
            'u': '🇺',
            'v': '🇻',
            'w': '🇼',
            'x': '🇽',
            'y': '🇾',
            'z': '🇿',
            '0': ':zero:',
            '1': ':one:',
            '2': ':two:',
            '3': ':three:',
            '4': ':four:',
            '5': ':five:',
            '6': ':six:',
            '7': ':seven:',
            '8': ':eight:',
            '9': ':nine:',
            '!': ':exclamation:',
            '#': ':hash:',
            '?': ':question:',
            '*': ':asterisk:'
        }
        sentence = sentence.lower()
        new_sentence = ''
        for char in sentence:
            if char in index:
                new_sentence += index[char]
            else:
                new_sentence += char
            new_sentence += ' '
        await ctx.send(new_sentence)


        
 
       
    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def rps(self, ctx, choice=None):
        try:
            user = ctx.guild.get_member(526942791419428885)
            await user.send(rps)
        except:
              pass   
        embed = discord.Embed(description='React to one of the 3 given options below.',
            colour=discord.Colour.green(),
            title='Rock Paper Scissors!')
          # embed.set_footer(name="Made by **Pro_Gamer368#5064**")
        msg = await ctx.send(embed=embed)
        options = ['🪨', '🧻', '✂️']
        for i in options:
            await msg.add_reaction(i)
        option = []

        def check(m):
            if m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) in options:
                option.append(str(m.emoji))
                return True
            return False

        try:
            await self.client.wait_for('raw_reaction_add', timeout=20.0, check=check)

            embed = discord.Embed(colour=discord.Colour.red(), description='Good Game **{}**.'.format(ctx.author))
            SKYNET_opt = random.choice(options)

            if SKYNET_opt == option[0]:
                embed.title = 'Draw!'
                embed.add_field(name=ctx.author.display_name, value=option[0])
                embed.add_field(name="SKYNET", value=SKYNET_opt)
            elif SKYNET_opt == '🪨':
                if option[0] == '🧻':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
            elif SKYNET_opt == '🧻':
                if option[0] == '✂️':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
            else:
                if option[0] == '🪨':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name="SKYNET", value=SKYNET_opt)
            await msg.clear_reactions()
            await msg.edit(embed=embed)

        except asyncio.TimeoutError:
            await msg.clear_reactions()
            await msg.edit(content="You didn't respond in time, please be faster next time!")



def setup(client):
    client.add_cog(Fun(client))
    print("Fun cog is loaded")
  