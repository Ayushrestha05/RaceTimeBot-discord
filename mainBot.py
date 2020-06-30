import discord
import csv
import pandas as pd
from discord.ext import commands

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print('Bot is ready to time!')


@bot.command(aliases=['yo'])  # aliases can be used to ping the same command with different name
async def ping(ctx):
    await ctx.send(f'Lets race against Time! \n Bot {round(bot.latency * 1000)}ms behind')


@bot.command()
async def time(ctx):
    emb = discord.Embed(title="Select the game that you are timing",
                        description="1. Forza Horizon 4 \n2. Need For Speed \n3. Asphalt 9", colour=0x3DF270)
    msg = await ctx.send(embed=emb)
    emoji_val = [":fh4:726417508868816976", ":nfs:726418023342145609", ":as9:726417878642851922"]
    # To get custom emoji id type \:emoji_name:
    for i in range(len(emoji_val)):
        await msg.add_reaction(emoji_val[i])

    @bot.event
    async def on_reaction_add(reaction, user):
        if ctx.author == user:
            if reaction.emoji.name == 'fh4':
                await ctx.channel.purge(limit=2)
                t1 = discord.Embed(title="Use /insert to insert track times", description="Syntax: /insert car,"
                                                                                          "car_power,track,time")
                await ctx.send(embed=t1)

                @bot.command()
                async def insert(ctx, *, args):
                    splitter = args.split(",")
                    car_user = "@" + str(ctx.author)
                    car_name = splitter[0]
                    car_power = splitter[1]
                    track_raced = splitter[2]
                    track_time = splitter[3]
                    with open('fh4trackstats.csv', 'a', newline='', encoding='utf-8') as f:
                        thewriter = csv.writer(f)
                        thewriter.writerow([car_user, car_name, car_power, track_raced, track_time])
            elif reaction.emoji.name == 'nfs':
                await ctx.channel.purge(limit=2)
            elif reaction.emoji.name == 'as9':
                await ctx.channel.purge(limit=2)


@bot.command()
async def laps(ctx):
    emb = discord.Embed(title="Select the game that you viewing Laps of",
                        description="1. Forza Horizon 4 \n2. Need For Speed \n3. Asphalt 9", colour=0x3DF270)
    msg = await ctx.send(embed=emb)
    emoji_val = [":fh4:726417508868816976", ":nfs:726418023342145609", ":as9:726417878642851922"]
    # To get custom emoji id type \:emoji_name:
    for i in range(len(emoji_val)):
        await msg.add_reaction(emoji_val[i])

    t2 = discord.Embed(title="Use /sort to sort track times", description="Syntax: /sort track_name")
    await ctx.send(embed=t2)

    @bot.event
    async def on_reaction_add(reaction, user):
        if ctx.author == user:
            if reaction.emoji.name == 'fh4':
                fh4TrackList = pd.read_csv('fh4trackstats.csv')

                @bot.command()
                async def sort(ctx, *, args):
                    filter_base = (fh4TrackList['Track'] == args)
                    await ctx.send(f'```{fh4TrackList[filter_base].sort_values(by="Time")}```')


bot.run('NzI2MDY1MDU5MDYyNjEyMDQx.Xvb8zw.xdmaxSH8SO8aTmXR8oagjl0p8XQ')  # Bot Token Inserted
