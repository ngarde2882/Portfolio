import discord
import random
import time
from discord.ext import commands

client = commands.Bot(command_prefix = 'p!')
# orderNo = [0]
# claim_list = []
# timeout = [0.0]


@client.event
async def on_ready():
    print('WonderBot is ready.')

# @client.command(aliases=['o'])
# async def order(message, platform, num=0000, *, ordr):
#     await message.send(f'Order: {num} has been placed! 5 minutes to claim!')
#     print('order', num, 'placed')
#     manager = message.author.id
#     orderNo[0] = num
#     timeout[0] = time.time() + 45  # 5 minutes from now
#     while timeout[0] >= time.time():
#         print('preclaim')
#         await claim()
#         print('postclaim')
#     print('time up')
#     if len(claim_list) == 0:
#         print('no claim')
#         await message.send(f'Y\'all are some bums, order {orderNo[0]} is first come, first serve'
#                            f'\nContact the manager that posted it')
#         orderNo[0] = 0
#         timeout[0] = 0
#         return
#     print('time to dish it out')
#     rando = len(claim_list)-1
#     rando = random.randint(0, rando)
#     winner = claim_list[rando]
#     await message.send(f'<@{manager}>, <@{winner}> has order {orderNo[0]}!')
#     orderNo[0] = 0
#     claim_list[0] = []
#     timeout[0] = 0
#     return

# @client.command(aliases=['c'])
# async def claim(ctx):
#     u = ctx.author.id
#     claim_list.append(u)
#     await ctx.send(f'<@{u}> is in the running for!')
#     return u

# @client.command(aliases=['cl'])
# async def clear(message):
#     await message.channel.purge()

# @client.command(aliases=['clovis'])
# async def banshee(ctx):
#     # call d2 api for banshee inventory
#     print('result1')

# @client.command(aliases=['ada-1'])
# async def ada(ctx):
#     # call d2 api for ada inventory
#     print('result2')

# @client.command(aliases=['x'])
# async def xur(ctx):
#     # call d2 api for xur inventory
#     print('result3')

# @client.command(aliases=['val'])
# async def valorant(ctx):
#     # call val api for player's shop
#     print('result4')

# @client.command(aliases=['fallguys','fallguy','fall'])
# async def fall_guys(ctx):
#     # call fall guys api for player shop
#     print('result5')

# @client.command(aliases=['init'])
# async def initialization(ctx):
#     # player creates a trainer account
#     print('init')

# @client.command(aliases=['catch'])
# async def catch(ctx):
#     # player attempts to catch pokemon
#     print('catch')

client.run('NzEzNDA0NzExNTcwNzY3OTk0.Xsg5_w.rcZZveDGpKKzztjcMpKpqowak5c')
