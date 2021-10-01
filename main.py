import discord
from discord.ext import commands
import os
import keepalive
# from discord_slash import SlashCommand

import random
import time
from time import sleep
import asyncio
from prsaw import RandomStuff
import json
from discord.ext.commands import when_mentioned_or
from itertools import cycle

# intents=intents
# intents = discord.Intents.all()

client = commands.Bot(command_prefix=when_mentioned_or("."))
client.remove_command('help')
# slash = SlashCommand(client, sync_commands = True)

async def status():
  while True:
    await client.wait_until_ready()

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.guilds)} Servers! |.help '))
    await asyncio.sleep(5)
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Happy birthday my developer SCHWITZ#3875(I am writing this for myself lmfao lack of co-workes XD)'))
    # await sleep(15)
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.users)} users |.help"))
    # await asyncio.sleep(5)
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Happy birthday 【𝔽𝕆】✨Death_Surfing#3093"))
    await asyncio.sleep(5)
    await client.loop.create_task(status())


@client.command()
async def su(ctx,member:discord.Member,*,msg):
  wh = await ctx.channel.create_webhook(name="lol")
  await ctx.message.delete()

  await wh.send(msg, username=member.display_name, avatar_url=member.avatar_url)
  await wh.delete()




mainshop = [{
    "name": "Watch",
    "price": 100,
    "description": "Time"
}, {
    "name": "Laptop",
    "price": 1000,
    "description": "Work"
}, {
    "name": "PC",
    "price": 10000,
    "description": "Gaming"
}, {
    "name": "Ferrari",
    "price": 99999,
    "description": "Sports Car"
}]
# @slash.slash()
# async def hello(ctx):
  # await ctx.send("Hello")

# @client.command()
# async def afk(ctx, mins):
#     current_nick = ctx.author.nick
#     await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.")
#     await ctx.author.edit(nick=f"{ctx.author.name} [AFK]")

#     counter = 0
#     while counter <= int(mins):
#         counter += 1
#         await asyncio.sleep(60)

#         if counter == int(mins):
#             await ctx.author.edit(nick=current_nick)
#             await ctx.send(f"{ctx.author.mention} is no longer AFK")
#             break




# rs = RandomStuff(api_key = "CyspHEdWQgQG" ,async_mode=True)
# @client.event
# async def on_message(message):
#   if client.user == message.author:
#     return
#   if message.channel.id == 804942896729686116:
#     response = await rs.get_ai_response(message.content)
#     await message.reply(response)
  
# @client.command
# async def joke(message):
#   if client.user == message.author:
#     return
#   if message.channel.id == 804942896729686116:
#     response = await rs.get_joke(message.content)
#     await message.reply(response)
# @slash.slash(description = "shows bal")
@client.command(aliases=['bal'])
async def balance(ctx):
	await open_account(ctx.author)
	user = ctx.author

	users = await get_bank_data()

	wallet_amt = users[str(user.id)]["wallet"]
	bank_amt = users[str(user.id)]["bank"]

	em = discord.Embed(title=f'{ctx.author.name} Balance',
	                   color=discord.Color.red())
	em.add_field(name="Wallet Balance", value=wallet_amt)
	em.add_field(name='Bank Balance', value=bank_amt)
	await ctx.send(embed=em)

@client.command()
async def checkmate(ctx):
  await ctx.send("https://tenor.com/view/anime-onepunchman-saitama-punchnuts-gif-4885033")


@client.command(pass_context=True)
async def serverinfo(ctx,member: discord.Member = None):
    """Displays server information."""
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0x176cd5)
    embed.add_field(name="Server Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.guild.members))
    embed.add_field(name="Channels", value=len(ctx.message.guild.channels))
    embed.add_field(name="Region", value=ctx.message.guild.region)
    embed.add_field(name="Verification Level", value=ctx.message.guild.verification_level)
    # embed.add_field(name="Owner", value=ctx.message.guild.owner.mention)
    embed.add_field(name="Emojis", value=len(ctx.message.guild.emojis))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
    # embed.set_footer(text="Server ID is " + ctx.message.guild.id)
    await ctx.send(embed=embed)




@client.event
async def when_mentioned(ctx):
    embed=discord.Embed(title="Hi, I'm Skynet", description="My default prefix is `.` or a mention. Hope this helps!", color=0x176cd5)
    await client.send_message(ctx.message.channel, embed=embed)
@client.event
async def on_command_error(ctx,error):
  if isinstance (error, commands.CommandOnCooldown):
    msg = ("***You are on cooldown!***, Please try again after {:.2f}s".format(error.retry_after))
    await ctx.send(msg)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
	await open_account(ctx.author)
	user = ctx.author

	users = await get_bank_data()

	earnings = random.randrange(101)

	await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

	users[str(user.id)]["wallet"] += earnings

	with open("mainbank.json", 'w') as f:
		json.dump(users, f)






@client.command(aliases=['wd'])
async def withdraw(ctx, amount=None):
	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[1]:
		await ctx.send('You do not have sufficient balance')
		return
	if amount < 0:
		await ctx.send('Amount must be positive!')
		return

	await update_bank(ctx.author, amount)
	await update_bank(ctx.author, -1 * amount, 'bank')
	await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


@client.command(aliases=['dp'])
async def deposit(ctx, amount=None):
	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[0]:
		await ctx.send('You do not have sufficient balance')
		return
	if amount < 0:
		await ctx.send('Amount must be positive!')
		return

	await update_bank(ctx.author, -1 * amount)
	await update_bank(ctx.author, amount, 'bank')
	await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


@client.command(aliases=['sm'])
async def send(ctx, member: discord.Member, amount=None):
	await open_account(ctx.author)
	await open_account(member)
	if amount == None:
		await ctx.send("Please enter the amount")
		return

	bal = await update_bank(ctx.author)
	if amount == 'all':
		amount = bal[0]

	amount = int(amount)

	if amount > bal[0]:
		await ctx.send('You do not have sufficient balance')
		return
	if amount < 0:
		await ctx.send('Amount must be positive!')
		return

	await update_bank(ctx.author, -1 * amount, 'bank')
	await update_bank(member, amount, 'bank')
	await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['rb'])
async def rob(ctx, member: discord.Member):
	await open_account(ctx.author)
	await open_account(member)
	bal = await update_bank(member)

	if bal[0] < 100:
		await ctx.send('It is useless to rob them :(')
		return

	earning = random.randrange(0, bal[0])

	await update_bank(ctx.author, earning)
	await update_bank(member, -1 * earning)
	await ctx.send(
	    f'{ctx.author.mention} You robbed {member} and got {earning} coins')







@client.command()
async def slots(ctx, amount=None):
	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[0]:
		await ctx.send('You do not have sufficient balance')
		return
	if amount < 0:
		await ctx.send('Amount must be positive!')
		return
	final = []
	for i in range(3):
		a = random.choice(['X', 'O', 'Q'])

		final.append(a)

	await ctx.send(str(final))

	if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
		await update_bank(ctx.author, 2 * amount)
		await ctx.send(f'You won :) {ctx.author.mention}')
	else:
		await update_bank(ctx.author, -1 * amount)
		await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
	em = discord.Embed(title="Shop")

	for item in mainshop:
		name = item["name"]
		price = item["price"]
		desc = item["description"]
		em.add_field(name=name, value=f"${price} | {desc}")

	await ctx.send(embed=em)


@client.command()
async def buy(ctx, item, amount=1):
	await open_account(ctx.author)

	res = await buy_this(ctx.author, item, amount)

	if not res[0]:
		if res[1] == 1:
			await ctx.send("That Object isn't there!")
			return
		if res[1] == 2:
			await ctx.send(
			    f"You don't have enough money in your wallet to buy {amount} {item}"
			)
			return

	await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()

	try:
		bag = users[str(user.id)]["bag"]
	except:
		bag = []

	em = discord.Embed(title="Bag")
	for item in bag:
		name = item["item"]
		amount = item["amount"]

		em.add_field(name=name, value=amount)

	await ctx.send(embed=em)


async def buy_this(user, item_name, amount):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			price = item["price"]
			break

	if name_ == None:
		return [False, 1]

	cost = price * amount

	users = await get_bank_data()

	bal = await update_bank(user)

	if bal[0] < cost:
		return [False, 2]

	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt + amount
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index += 1
		if t == None:
			obj = {"item": item_name, "amount": amount}
			users[str(user.id)]["bag"].append(obj)
	except:
		obj = {"item": item_name, "amount": amount}
		users[str(user.id)]["bag"] = [obj]

	with open("mainbank.json", "w") as f:
		json.dump(users, f)

	await update_bank(user, cost * -1, "wallet")

	return [True, "Worked"]


@client.command()
async def sell(ctx, item, amount=1):
	await open_account(ctx.author)

	res = await sell_this(ctx.author, item, amount)

	if not res[0]:
		if res[1] == 1:
			await ctx.send("That Object isn't there!")
			return
		if res[1] == 2:
			await ctx.send(f"You don't have {amount} {item} in your bag.")
			return
		if res[1] == 3:
			await ctx.send(f"You don't have {item} in your bag.")
			return

	await ctx.send(f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			if price == None:
				price = 0.7 * item["price"]
			break

	if name_ == None:
		return [False, 1]

	cost = price * amount

	users = await get_bank_data()

	bal = await update_bank(user)

	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt - amount
				if new_amt < 0:
					return [False, 2]
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index += 1
		if t == None:
			return [False, 3]
	except:
		return [False, 3]

	with open("mainbank.json", "w") as f:
		json.dump(users, f)

	await update_bank(user, cost, "wallet")

	return [True, "Worked"]


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=1):
	users = await get_bank_data()
	leader_board = {}
	total = []
	for user in users:
		name = int(user)
		total_amount = users[user]["wallet"] + users[user]["bank"]
		leader_board[total_amount] = name
		total.append(total_amount)

	total = sorted(total, reverse=True)

	em = discord.Embed(
	    title=f"Top {x} Richest People",
	    description=
	    "This is decided on the basis of raw money in the bank and wallet",
	    color=discord.Color(0xfa43ee))
	index = 1
	for amt in total:
		id_ = leader_board[amt]
		member = client.get_user(id_)
		name = member.name
		em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
		if index == x:
			break
		else:
			index += 1

	await ctx.send(embed=em)


async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open('mainbank.json', 'w') as f:
		json.dump(users, f)

	return True


async def get_bank_data():
	with open('mainbank.json', 'r') as f:
		users = json.load(f)

	return users


async def update_bank(user, change=0, mode='wallet'):
	users = await get_bank_data()

	users[str(user.id)][mode] += change

	with open('mainbank.json', 'w') as f:
		json.dump(users, f)
	bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
	return bal


@client.command()
async def ping(ctx):
	# await ctx.send(f'Pong {round(client.latency*1000)}ms')
	embed = discord.Embed(Title="🏓 Ping",
	                      color=discord.Colour.green())
	embed.add_field(
	    name="API Ping",
	    value=f"🏓 {round(client.latency*1000)}ms")
	await ctx.send(embed=embed)


@client.event
async def on_msg(ctx, msg):
	if ':' == msg.content[0] and ':' == msg.content[-1]:
		emoji_name = msg.content[1:-1]
		for emoji in msg.guild.emojis:
			if emoji_name == emoji.name:
				await msg.delete()
				await ctx.send(str(emoji))
				break







def convert(time):
  pos = ['s','m','h','d']

  time_dict = {'s' :1, 'm' :60, 'h' : 3600 , 'd' : 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2
    return val * time_dict[unit]



@client.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx):
  
  await ctx.send("Let's start with this Giveaway! Answer these questions within 25 seconds.")
  questions = ["Which channel should it be hosted in?",
                "What should be the duration of the Giveaway?",
                "What is the price of the Giveaway?"]
  answers = []

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel


  for i in questions:
    await ctx.send(i)

    try:  
      msg = await client.wait_for('message', timeout=25.0, check=check)
    except asyncio.TimeoutError:
      await ctx.send("You didn't answer in time, please retry and be quicker this time!")
      return
    else:
      answers.append(msg.content)
        
    try:
      c_id = int(answers[0][2:-1])
    except:
      await ctx.send(f"You didn't mention a channel properly, do like this {ctx.channel.mention}")
      return
    
  channel = client.get_channel(c_id)

  time = convert(answers[1])

  if time == -1:
    await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d)")
    return
  elif time == -2:
    await ctx.send("The time must be an Integer. Please enter an integer next time.")
    return
  prize = answers[2]

  # await ctx.send(f"The Giveaway well be in {channel.mentoin} and will last for {answers[1]} seconds!")

  embed = discord.Embed(title = "Giveaway!", description =f"{prize}", color = ctx.author.color)
  embed.add_field(name = f"Hosted by:", value = ctx.author.mention)
  embed.set_footer(text = f"Ends {answers[1]} from now!")

  my_msg = await channel.send(embed=embed)
  await my_msg.add_reaction("🎊")
  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reaction[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

	print('Servers connected to:')
	for guild in client.guilds:
		print(f"{guild.name}\n{len(guild.members)}")
	client.loop.create_task(status())


f = open("rules.txt", "r")
rules = f.readlines()


@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'Loaded {extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')


@load.error
async def load_error(ctx, error):
	await ctx.send('Invalid use of command')





keepalive.keepalive()
TOKEN = os.environ.get("TOKEN")
client.run(TOKEN)
