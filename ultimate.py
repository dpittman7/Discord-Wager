import discord
import random
import linecache
import re
import shelve
import copy
import math
from random import shuffle, randint
from datetime import datetime
from discord.ext import commands
from utilities import datadriver
import web3_logic
import functools
import typing
import asyncio
import requests
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
reaction = discord.Reaction

ETHERSCAN_TOKEN= os.getenv('ETHERSCAN_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CURRENT_CONTRACT = os.getenv('CONTRACT_ADDY')
POLL_INTERVAL = 5
RANK_THRESHOLD = 100
#RANKLIST = treeSet.TreeSet()
FILENAME = os.getenv('FILENAME')
dataframe = datadriver.loadTable(FILENAME)

@client.event

async def on_ready():
    guild_list = client.guilds #sees all the users that the bot can see.

    #guild = discord.utils.find(lambda m: m.guild == 'Ultimate', guild_list)
    #active_role = discord.utils.find(lambda m: m.role == 'Active', guild.roles)
    #active_members = active_role.members

    dataframe = datadriver.loadTable(FILENAME)
    spliceframe = dataframe.iloc[:,[0,5]] #creates dataframe with only USERNAME and RANK as columns. Still row indexed by ID
    print(spliceframe)

    

    #make key-value pair object | ranking (key) -> userID (value) | populate TreeSet with ranking as header.




    print(guild_list)
    print('We have logged in as {0.user}'.format(client))

    while True:
        channel = client.get_channel(1014955523176669314)
        result = await contractLogger(channel)
        await asyncio.sleep(POLL_INTERVAL)
        #print(result)

#create an object that stores all the memebrs in a guild/server



#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
#
#####################################################################

@client.event    
async def on_message(message):

    
    #Not implemented
    #challenge confirmation system: To throw exception when the user is
    #actively under a discord command
    
    #change users roles when in challenge -
    # use role as trigger to restrict user from initating challenge command
    
    #Need to abstractify scope of server. i.e have driving logic to identify 
    
    if message.author == client.user:
        return
    print(*client.guilds) #extract message's guild for expansion
    print(message.content)
    
    if message.content.startswith('!challenge'):
        dataframe = datadriver.loadTable(FILENAME)
        if(not datadriver.getUserValue(dataframe,message.author.id,'IN_CHALLENGE')):
            await challenge(client, message, reaction)
        else:
            await message.channel.send("Challenge currently in progress")

    if message.content.startswith('!wager'):
        dataframe = datadriver.loadTable(FILENAME)
        if(not datadriver.getUserValue(dataframe,message.author.id,'IN_CHALLENGE')):
            await challenge(client, message, reaction, 1)
        else:
            await message.channel.send("Challenge currently in progress")

    if message.content.startswith('!stats'):
        await stats(message)
        
    if message.content.startswith('!login'):
        await login(client, message)
    
    if message.content.startswith('!logout'):
        await logout(client, message)
        
    if message.content.startswith('!rank'):
        await callRank(message)

    if message.content.startswith('!initialize'):
        print("Initializing User")
        await initializeUser(client, message)                                                                                                                                                                                                                                                                         


#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def contractLogger(channel):
    result = await web3_logic.pullWatcher()
    addUser_log, withdrawFunds_log, depositFunds_log, rankUpdated_log, balanceUpdated_log = result.result()
    print(rankUpdated_log)


    for addy in addUser_log:
        #EXTRACT DATA
        e = discord.Embed(title = 'Contract Event Emit', description='Added User', url = 'https://rinkeby.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        
        await channel.send(embed=e)
        #Need to integrate into initiaize function
        #DISPLAY
    for addy, withdrawl, userBalance in withdrawFunds_log:
        

        e = discord.Embed(title = 'Contract Event Emit', description='Credit Withdrawl', url = 'https://rinkeby.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Withdrawl Amount', value='{} Wei'.format(withdrawl), inline = True)
        e.add_field(name='Current Balance', value='{} Wei'.format(userBalance), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        
        await channel.send(embed=e)

        print(addy)
        print(withdrawl)
        print(userBalance)

        #DISPLAY
    for addy, depositAmount, userBalance in depositFunds_log:

        print("inside Embed Formation")
        e = discord.Embed(title = 'Contract Event Emit', description='Credit Deposit', url = 'https://rinkeby.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Deposit Amount', value='{} Wei'.format(depositAmount), inline = True)
        e.add_field(name='Current Balance', value='{} Wei'.format(userBalance), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        await channel.send(embed=e)


        print(addy)
        print(depositAmount)
        print(userBalance)

    for addy, rank in rankUpdated_log:

        print("inside Embed Formation")
        e = discord.Embed(title = 'Contract Event Emit', description='User Rank Updated', url = 'https://rinkeby.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Current Rank', value='{}'.format(rank), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        await channel.send(embed=e)


        print(addy)
        print(rank)
       
    
    for addy, balance in balanceUpdated_log:

        print("inside Embed Formation")
        e = discord.Embed(title = 'Contract Event Emit', description='User Balance Updated', url = 'https://rinkeby.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Current Balance', value='{} Wei'.format(balance), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        await channel.send(embed=e)


        print(addy)
        print(balance)
        

    #print("returning task contractLogger() - {}".format(result.result()))
         
        

#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

#lazy code, will need to update it for the bot to be mass launched.
async def login(client, message):
    user = message.author

    #ADD: Check if the user has role "In Match" - Send Error Message and terminate function.
   
    
    role = discord.utils.get(client.guilds[0].roles, name="Active")
    await user.add_roles(role)
    
    role = discord.utils.get(client.guilds[0].roles, name="Inactive")
    await user.remove_roles(role)


#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

#will need to add timeout when launched onto external server    
async def logout(client, message):

    #ADD: Check if the user has role "In Match" - Send Error Message and terminate function.

    user = message.author

    role = discord.utils.get(client.guilds[0].roles, name="Inactive")
    await user.add_roles(role)
    
     
    role = discord.utils.get(client.guilds[0].roles, name="Active")
    await user.remove_roles(role)

#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################
def toggleInChallenge(userID, toggle):
    df = datadriver.loadTable(FILENAME)
    datadriver.updateUserValue(df,userID,'IN_CHALLENGE',toggle)
    

#####################################################################
# Function:
# Parameters:
#
# Behavior: Retreives message sender rank
#
# Returns:
# Author: Deanta Pittman
#
# Notes:
#####################################################################   
           
async def callRank(message):
    dataframe = datadriver.loadTable(FILENAME)
    rank = datadriver.getUserValue(dataframe,message.author.id,'RANK')
    await message.channel.send('Current Rank: {}'.format(rank))

#####################################################################
# Function:
# Parameters:
#
# Behavior: Retreives block value of balance
#
# Returns:
# Author: Deanta Pittman
#
# Notes: will need to add timer function when launched onto external server
#####################################################################  




async def callBalance(message):
    dataframe = datadriver.loadTable(FILENAME)
    addy = datadriver.getUserValue(dataframe,message.author.id,'ETH_ADDY')
    if web3_logic.isUser(addy):
        balance = web3_logic.getBalance(addy)
        await message.channel.send('Current Balance: {}'.format(balance))
    else:
        await message.channel.send('Please set addy first.')   

#####################################################################
# Function:
# Parameters:
#
# Behavior: sets user's ethereum wallet address for web3_logic lookup functions
#
# Returns:
# Author: Deanta Pittman
#
# Notes: Implement questioning in user DM's
#####################################################################  

async def initializeUser(client, message):
    await message.channel.send('Enter the Ethereum address that will be synced with this server')
    answer = 0
    attempts = 0
    while(not answer):
        
        reply = await client.wait_for('message') # Replace waiting for user input and implement set gamecount by react.     
        if reply.author.id == message.author.id:
            #Need to add logic to validate user inputted address
            dataframe = datadriver.loadTable(FILENAME)
            datadriver.addUser(dataframe,message.author.id,message.author.name,reply.content,FILENAME)
            web3_logic.addUser(reply.content)
            await message.channel.send('User added, welcome to the mix {}!'.format(message.author.name))
            answer = 1
        
#add rank difference to eligible function
#gamelist[0] - challengerID , gamelist[1] = challengedID
async def eligible(message, gamelist,wagerValue):
    eligible = 0
    dataframe = datadriver.loadTable(FILENAME)
    try:
        challengerAddy = datadriver.getUserValue(dataframe,gamelist[0],'ETH_ADDY')
        challengedAddy = datadriver.getUserValue(dataframe,gamelist[0],'ETH_ADDY')
        if challengerAddy != "" and challengerAddy != "":
            print("evaluating web3 stats")
            balance1 = web3_logic.getBalance(challengerAddy)
            balance2 = web3_logic.getBalance(challengedAddy)
            print(" User Balances - {0} | {1}".format(balance1,balance2))

            rank1 = web3_logic.getRank(challengerAddy)
            rank2 = web3_logic.getRank(challengedAddy)
            rankDifference = abs(rank1-rank2)
            print(" User Rank - {0} | {1} | diff - {2}".format(rank1,rank2,rankDifference))
         

            if balance1 > wagerValue and balance2 > wagerValue and rankDifference < RANK_THRESHOLD:
                print("eligibility passed")
                eligible = 1
            else:
                print("Failed eligibility")
    except:
        print('error in elgibility attempt')

    return eligible


async def selectWager(message,gamelist):
    

    r = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey={}'.format(ETHERSCAN_TOKEN))
    ethprice = float(r.json()["result"]["ethusd"])
    print(ethprice)
    challengerUser = message.author.name
    challengedUser = message.mentions[0].name
    e = discord.Embed(title = 'Select Wager Amount', color=discord.Color.yellow())
    e.add_field(name='.001 Ether', value='~ {} USD'.format(ethprice*.001), inline = True)
    e.add_field(name='.003 Ether', value='~ {} USD'.format(ethprice*.003), inline = True)
    e.add_field(name='.005 Ether', value='~ {} USD'.format(ethprice*.005), inline = True)
    e.add_field(name='{} Selection'.format(challengerUser), value='X', inline = False)
    e.add_field(name='{} Selection'.format(challengedUser), value='X', inline = False)
    e.set_footer(text='React to choose your selection', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
    activeEmbed = await message.channel.send(embed=e)

    await activeEmbed.add_reaction(str('1️⃣')) #unicode for 100 points
    await activeEmbed.add_reaction(str('3️⃣')) #unicode for cross mark
    await activeEmbed.add_reaction(str('5️⃣')) #unicode for cross mark
    value = 0
    selection = 0
    challengersChoice = -1
    oppositionsChoice = -2

    while(not selection):
    
        reactEvent = await client.wait_for('reaction_add')#create fail case
        #print(reactEvent)
        reaction = reactEvent[0]
        print(reaction) #Reaction Object of awaited react event
        reactorID = reactEvent[1].id # ID of reactor
        print(reactorID)

        print(gamelist)

        #Evaluating Challengers Choice 
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('1️⃣'):
            e.set_field_at(index=3,name='{}'.format(challengerUser),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 1
            
            
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=3,name='{}'.format(challengerUser),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 3

        if reactorID == gamelist[0] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=3,name='{}'.format(challengerUser),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 5

        #Evaluating Opposition Choice 
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('1️⃣'):
            e.set_field_at(index=4,name='{}'.format(challengedUser),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 1
            
            
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=4,name='{}'.format(challengedUser),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 3

        if reactorID == gamelist[1] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=4,name='{}'.format(challengedUser),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 5

        await asyncio.sleep(1)
        print('{0} - {1}'.format(challengersChoice,oppositionsChoice))

        if oppositionsChoice == challengersChoice:
            e = discord.Embed(title = 'Wager Amount Selected', color=discord.Color.green())
            e.add_field(name='.00{} Ether'.format(oppositionsChoice), value='approx {} USD'.format(ethprice*.001), inline = True)
            e.set_footer(text='The wager will begin shortly.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
            activeEmbed = await activeEmbed.edit(embed=e)
            await activeEmbed.delete(delay=5.0)
            value = oppositionsChoice * 1000000000000000
            selection = 1
    
    return value






#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def challenge(client, message, reaction, wager = 0): #mainloop
    #Declarations
    gamelist = [] #gamelist[0] - challengerID , gamelist[1] = challengedID
    status_state = [0,0,0,0,0] #game[0] - state. game[1] - gamecount, game[2] - win state, game[3] -challenger_wincount, game[4] - opponent_wincount
    date = datetime.date #date object to get date of posting the embed
    value = 0
    gamelist, challengerData, oppositionData = await initialize(client,message)
    if(wager):
        value = await selectWager(message,gamelist)
        if not await eligible(message, gamelist, value):
            errorMessage = await message.channel.send("A user is unelgible for wager matches, ensure all parties meet the requirements defined in #how-to-use")
            await errorMessage.delete(delay=10.0)
            status_state[0] = await terminate(gamelist,message)
            
    
    print(0)
    #print(gamelist[1])
    if status_state[0] == 0:  status_state, activeEmbed = await confirm(client, message, gamelist, status_state, reaction, wager, value)
    print(status_state[0])
    if status_state[0] == 2: await gamecount(client, message, status_state, gamelist, activeEmbed)
    while (status_state[0] == 3 or status_state[0] == 4):
        if status_state[0] == 3: await inprogress(client,message,gamelist, status_state, wager, value,activeEmbed)
        if status_state[0] == 4: await postresult(client,message,gamelist, status_state, date, wager, value)


    if status_state[0] == -1 :
        termination_message = await message.channel.send('Challenge Terminated')
        await termination_message.delete(delay=3)


#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################
    
async def confirm(client, message, gamelist, status_state, reaction, wager = 0, value = 0):
    #confirm challenge
    gamelist, challengerStats, oppositionStats = await initialize(client,message)
    print('gamelist {}'.format(*gamelist))
    status_state[0] = 1


    #Create Embed
    e = discord.Embed(title = 'Challenge', color=discord.Color.yellow())
    e.add_field(name='CHALLENGER', value=challengerStats[0], inline = False)
    e.add_field(name='RANK', value=challengerStats[1], inline = True)
    e.add_field(name='WINS', value=challengerStats[2], inline = True)
    e.add_field(name='STREAK', value=challengerStats[3], inline = True)
    e.add_field(name='vs', value=" --- pending --- ", inline = False)
    e.add_field(name='OPPOSITION', value=oppositionStats[0], inline = False)
    e.add_field(name='RANK', value=oppositionStats[1], inline = True)
    e.add_field(name='WINS', value=oppositionStats[2], inline = True)
    e.add_field(name='STREAK', value=oppositionStats[3], inline = True)
    if wager:
        e.add_field(name='WAGER VALUE', value=value, inline = False)
    e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')

    
    challengeEmbed = await message.channel.send(embed=e)
    await challengeEmbed.add_reaction(str('✅')) #unicode for 100 points
    await challengeEmbed.add_reaction(str('⛔')) #unicode for cross mark
    while status_state[0] == 1:
      #  print(1)
        reactEvent = await client.wait_for('reaction_add')#create fail case
        print(reactEvent)
        reaction = reactEvent[0]
        print(reaction) #Reaction Object of awaited react event
        reactorID = reactEvent[1].id # ID of reactor

        print("------------")
        print(reactorID)
        print(gamelist[1])
        print(reactEvent[0])

        #loose logic - expected to be prone to bugs
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('✅'):
            e.color=discord.Color.green()
            e.set_field_at(index=4,name='vs',value=" --- accepted ----")
            challengeEmbed = await challengeEmbed.edit(embed=e)
            await challengeEmbed.clear_reaction(str('✅')) #unicode for 100 points
            await challengeEmbed.clear_reaction(str('⛔')) #unicode for cross mark
            #await message.channel.send('The challenger arives, welcome.'.format(gamelist[0]))
            status_state[0] = 2
            
        if (reactorID == gamelist[1] or reactorID == gamelist[0]) and str(reactEvent[0]) == str('⛔'):
            e.color=discord.Color.red()
            if reactorID == gamelist[0]:
                e.set_field_at(index=4,name='vs',value=" --- aborted ----")
            else:
                e.set_field_at(index=4,name='vs',value=" --- rejected ----")
            challengeEmbed = await challengeEmbed.edit(embed=e)
            await challengeEmbed.clear_reaction(str('✅')) #unicode for 100 points
            await challengeEmbed.clear_reaction(str('⛔')) #unicode for cross mark
            #await message.channel.send('Maybe next time')
            status_state[0] = await terminate(gamelist,message) 

    await asyncio.sleep(3)
    return status_state, challengeEmbed    
    

#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def gamecount(client, message, status_state, gamelist, activeEmbed): #strip gamecount.
    #state gamecount
    print(5)
    #print(status_state[0])
    gamelist, challengerStats, oppositionStats = await initialize(client,message)

    challengersChoice = -2
    oppositionsChoice = -1
    abort = 0
    e = discord.Embed(title = 'Select GameCount', color=discord.Color.yellow())
    e.add_field(name='{}'.format(challengerStats[0]), value='X', inline = True)
    e.add_field(name='{}'.format(oppositionStats[0]), value='X', inline = True)
    e.set_footer(text='React to choose your selection', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
    
    await activeEmbed.edit(embed=e)
    await activeEmbed.add_reaction(str('1️⃣')) #unicode for 100 points
    await activeEmbed.add_reaction(str('3️⃣')) #unicode for cross mark
    await activeEmbed.add_reaction(str('5️⃣')) #unicode for cross mark
    await activeEmbed.add_reaction(str('❌')) #unicode for cross mark
    while status_state[0] == 2 and not abort:
        
        reactEvent = await client.wait_for('reaction_add')#create fail case
        print(reactEvent)
        reaction = reactEvent[0]
        print(reaction) #Reaction Object of awaited react event
        reactorID = reactEvent[1].id # ID of reactor

        print("------------")
        print(reactorID)
        print(gamelist[1])
        print(reactEvent[0])

        
        #Evaluating Challengers Choice 
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('1️⃣'):
            e.set_field_at(index=0,name='{}'.format(challengerStats[0]),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 1
            
            
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=0,name='{}'.format(challengerStats[0]),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 3

        if reactorID == gamelist[0] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=0,name='{}'.format(challengerStats[0]),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = 5
        
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('❌'):
            e.set_field_at(index=0,name='{}'.format(challengerStats[0]),value="ABORTED")
            activeEmbed = await activeEmbed.edit(embed=e)
            challengersChoice = -1

        #Evaluating Opposition Choice 
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('1️⃣'):
            e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 1
            
            
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 3

        if reactorID == gamelist[1] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 5
        
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('❌'):
            e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="ABORTED")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = -1

        await asyncio.sleep(1)
        print('{0} - {1}'.format(challengersChoice,oppositionsChoice))

        if oppositionsChoice == -1 or challengersChoice == -1:
            abort = 1
            await activeEmbed.delete(delay=7.0)
            status_state[0] = await terminate(gamelist,message)



        if oppositionsChoice == challengersChoice and not abort:

            e = discord.Embed(title = 'Challenge:', color=discord.Color.green())
            e.add_field(name='CHALLENGER', value=challengerStats[0], inline = False)
            e.add_field(name='RANK', value=challengerStats[1], inline = True)
            e.add_field(name='WINS', value=challengerStats[2], inline = True)
            e.add_field(name='STREAK', value=challengerStats[3], inline = True)
            e.add_field(name='vs', value="BEST OF {}".format(oppositionsChoice), inline = False)
            e.add_field(name='OPPOSITION', value=oppositionStats[0], inline = False)
            e.add_field(name='RANK', value=oppositionStats[1], inline = True)
            e.add_field(name='WINS', value=oppositionStats[2], inline = True)
            e.add_field(name='STREAK', value=oppositionStats[3], inline = True)
            e.set_footer(text='The Battle Begins', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')

            await activeEmbed.edit(embed=e)
            await activeEmbed.clear_reaction(str('1️⃣')) #unicode for 100 points
            await activeEmbed.clear_reaction(str('3️⃣')) #unicode for cross mark
            await activeEmbed.clear_reaction(str('5️⃣')) #unicode for cross mark
            await activeEmbed.clear_reaction(str('❌')) #unicode for cross mark

            
            status_state[2] =  oppositionsChoice  #gamecount
            status_state[0] = 3



#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def inprogress(client, message, gamelist,status_state,wager = 0 , value = 0, activeEmbed=discord.message):
    gamelist, challengerStats, oppositionStats = await initialize(client,message)
    challenger_ID = gamelist[0]
    challenged_ID = gamelist[1]
    print(challenger_ID)
    print(challenged_ID)
    print(status_state)
    
    
    challenger_name = message.author.name
    challenged_name = message.mentions[0].name

    wontheSet = int(1 + math.floor(int(status_state[2]) / 2))
    
    
    #skipcheck = 0 
    #await message.channel.send('admin check, skip phase?')
    #reply = await client.wait_for('message')
    #if reply.author.name == 'unterrorize' and reply.content == 'skip':
    #   skipcheck = 1
       
    #if skipcheck != 1:
    abort = 0
    concluded = 0
    for games in range(int(status_state[2])):
            
            if abort or concluded:
                continue


            title = 'Game Number ' + str(games) + ':'
            e = discord.Embed(title = 'Challenge: {0} vs {1}'.format(challengerStats[0],oppositionStats[0]))
            e.add_field(name= 'Game Number', value=(games + 1), inline=False)
            e.add_field(name=challenger_name, value = status_state[3], inline = True)
            e.add_field(name=challenged_name, value = status_state[4], inline = True)
            e.set_footer(text='WINNER SAY win IN CHAT TO CLAIM WIN, opponent either type confirm or deny.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
            await activeEmbed.edit(embed = e)
            game_confirm = 0
            confirm_check = 0
            
            while game_confirm == 0:
                

               winconfirm = await client.wait_for('message')
               
               if (winconfirm.author.id == challenger_ID or winconfirm.author.id == challenged_ID) and winconfirm.content == 'abort':
                abort = await abortCheck(winconfirm,gamelist,challengerStats[0],oppositionStats[0]) 
                
                
               #challenger wins match
               if winconfirm.author.id == challenger_ID and winconfirm.content == 'win':
                confirmation_requesta = await message.channel.send('challenged, confirm.')
                
                while confirm_check == 0 and not abort:
                    confirmation_submission = await client.wait_for('message')


                    if confirmation_submission.author.id == challenged_ID and confirmation_submission.content == 'confirm':
                        confirm_check = 1
                        status_state[3] += 1
                        await updaterecord(challenger_ID,challenged_ID)
                        game_confirm = 1
                        await confirmation_submission.add_reaction(str('👍'))
                        await winconfirm.delete(delay=2.0)
                        await confirmation_requesta.delete(delay=1.5)
                        await confirmation_submission.delete(delay=1.0)

                    if confirmation_submission.author.id == challenged_ID and confirmation_submission.content == 'deny':
                        abort = await abortCheck(winconfirm,gamelist,challengerStats[0],oppositionStats[0])
                        confirm_check = 1
                        game_confirm = 1
                        await confirmation_submission.add_reaction(str('👍'))
                        await winconfirm.delete(delay=2.0)
                        await confirmation_requesta.delete(delay=1.5)
                        await confirmation_submission.delete(delay=1.0)
                        
               #challenged wins match         
               if winconfirm.author.id == challenged_ID and winconfirm.content == 'win' and not abort:
                confirmation_requestb = await message.channel.send('challenger, confirm.')
               
            
                while confirm_check == 0:
                    confirmation_submission = await client.wait_for('message')

                    if confirmation_submission.author.id == challenger_ID and confirmation_submission.content == 'confirm':
                        confirm_check = 1
                        status_state[4] += 1
                        await updaterecord(challenged_ID,challenger_ID)
                        game_confirm = 1
                        await confirmation_submission.add_reaction(str('👍'))
                        await winconfirm.delete(delay=5.0)
                        await confirmation_requestb.delete(delay=5.0)
                        await confirmation_submission.delete(delay=1.0)
                    
                    if confirmation_submission.author.id == challenger_ID and confirmation_submission.content == 'deny':
                        abort = await abortCheck(winconfirm,gamelist,challengerStats[0],oppositionStats[0])
                        confirm_check = 1
                        game_confirm = 1
                        await confirmation_submission.add_reaction(str('👍'))
                        await winconfirm.delete(delay=2.0)
                        await confirmation_requesta.delete(delay=1.5)
                        await confirmation_submission.delete(delay=1.0)

                    


            if status_state[3] == wontheSet or status_state[4] == wontheSet:
                concluded = 1
                await message.channel.send('Game match reached! Winner is decided')
           
            if status_state[3] == wontheSet:
                await updaterecord(challenger_ID,challenged_ID, wager, value) #When status state 3 == status state 2, challenger has won.
            if status_state[4] == wontheSet:
                await updaterecord(challenged_ID,challenger_ID, wager, value)
    
    if abort:
        status_state[0] = await terminate(gamelist,message)
    else:
        status_state[0] = 4


#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def postresult(client,message,gamelist,status_state,date, wager = 0, value = 0):
    print('posting results in message channel')

    dataframe = datadriver.loadTable(FILENAME)
    challenger_name = message.author.name
    challenged_name = message.mentions[0].name
    challenger_rank = datadriver.getUserValue(dataframe,message.author.id,'RANK')
    challenged_rank = datadriver.getUserValue(dataframe,message.mentions[0].id,'RANK')
    time = datetime.now()
    
    e = discord.Embed(title = 'Challenge Results: ' + challenger_name + ' vs ' + challenged_name, description = 'Best of ' + str(status_state[1]))
    e.set_footer(text= 'Time of completion: ' + str(time) )
    e.add_field(name='{0} - {1}'.format(challenger_name, challenger_rank), value = status_state[3], inline = True)
    e.add_field(name='{0} - {1}'.format(challenged_name, challenged_rank), value = status_state[4], inline = True)
    
    channel = client.get_channel(861363885747470337)
    await channel.send(embed=e)

    datadriver.updateUserValue(dataframe,gamelist[0],'IN_CHALLENGE',0)
    datadriver.updateUserValue(dataframe,gamelist[1],'IN_CHALLENGE',0)
    status_state[0] = 5

#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes:
#####################################################################

async def initialize(client,message):
    #inital message will determine playerlist
    playerlist = []
    challengerID = message.author.id
    challengedID = message.mentions[0].id
    playerlist.append(challengerID)
    playerlist.append(challengedID)
    

    dataframe = datadriver.loadTable(FILENAME)
    challengerStats = []
    challengerStats.append(datadriver.getUserValue(dataframe,playerlist[0],'USERNAME'))
    challengerStats.append(datadriver.getUserValue(dataframe,playerlist[0],'RANK'))
    challengerStats.append(datadriver.getUserValue(dataframe,playerlist[0],'WINS'))
    challengerStats.append(datadriver.getUserValue(dataframe,playerlist[0],'STREAK'))

    oppositionStats = []
    oppositionStats.append(datadriver.getUserValue(dataframe,playerlist[1],'USERNAME'))
    oppositionStats.append(datadriver.getUserValue(dataframe,playerlist[1],'RANK'))
    oppositionStats.append(datadriver.getUserValue(dataframe,playerlist[1],'WINS'))
    oppositionStats.append(datadriver.getUserValue(dataframe,playerlist[1],'STREAK'))

    #SETS IN_CHALLENGE TO 1, USED IN NEGATING USERS CALLING OTHER COMMANDS WHILE IN CHALLENGE
    toggleInChallenge(challengerID,1)
    toggleInChallenge(challengedID,1)


    return playerlist, challengerStats, oppositionStats
    

#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes:
#####################################################################
 
async def update_state(status_state,state=0, gamecount=0,winstate=0,challenger_wincount = 0, challenged_wincount = 0):
    status_state_temp = status_state
    print(0)
    if state == 2 :
        status_state[0] = 2
    elif state == 1:
        status_state[0] += 1
    if gamecount != 0 :
        status_state[1] += 1
    if winstate != 0 :
        status_state[2] = winstate
    if challenger_wincount != 0 :
        status_state[3] += 1
    if challenged_wincount != 0 :
        status_state[4] += 1
    
    return status_state_temp


#####################################################################
# Function:
# Parameters:
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes:
#####################################################################

async def terminate(gamelist, message):
    abortMessage = await message.channel.send('Challenged aborted, until next time.')
    toggleInChallenge(gamelist[0],0)
    toggleInChallenge(gamelist[1],0)
    await abortMessage.delete(delay=5.0)
    return -1

async def abortCheck(message,gamelist,username1,username2):
    abort = 0
    abortMessage = await message.channel.send('Challenge will be aborted and marked for admin review. Any suspecion of ill-practice will result in a ban. confirm?')
    await abortMessage.add_reaction(str('✅')) #unicode for 100 points
    await abortMessage.add_reaction(str('⛔')) #unicode for cross mark



    abortConfirmation = 0
    while(not abortConfirmation):
        reactEvent = await client.wait_for('reaction_add')

        reaction = reactEvent[0]
        print(reaction) #Reaction Object of awaited react event
        reactorID = reactEvent[1].id # ID of reactor

        if (reactorID == gamelist[0] or reactorID == gamelist[1]) and str(reaction) == str('✅'):
            abort = 1
            abortConfirmation = 1
            e = discord.Embed(title = 'Challenge: {0} vs {1}'.format(username1,username2), color=discord.Color.red())
            e.add_field(name= 'ABORTED', value='-', inline=False)
            e.set_footer(text='WHO DARES INTERRUPTS GLORY? - DONT LET IT HAPPEN AGAIN, __we will be watching__', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
            await message.channel.send(embed=e)
            
        if (reactorID == gamelist[0] or reactorID == gamelist[1]) and str(reaction) == str('⛔'):
            await abortMessage.add_reaction(str('👍')) 
            o = await message.channel.send('Back to the challenge then, quit playing around and defeat your enemy!')
            abortConfirmation = 1
            await message.delete(delay=3.0)
            await abortMessage.delete(delay=3.0)
            await o.delete(delay=3.0)
    
    return abort

    

#####################################################################
# Function: async def updaterecord(winner_ID, loser_ID)
# Parameters: winner_ID/loser_ID -> int discord user ID's
#             
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: implement pandas to mature file-based database ~ Replacing text files with csv file
#####################################################################
#updaterecord(355178090231758850,355178090231758850,1,10000)

async def updaterecord(winner_ID,loser_ID, wager = 0, value = 0):

    dataframe = datadriver.loadTable(FILENAME)
    datadriver.updateUserValue(dataframe,winner_ID,'WINS')
    datadriver.updateUserValue(dataframe,loser_ID,'LOSES')

    datadriver.updateUserValue(dataframe,winner_ID,'TOTAL')
    datadriver.updateUserValue(dataframe,loser_ID,'TOTAL')

    datadriver.updateUserValue(dataframe,winner_ID,'STREAK')
    datadriver.updateUserValue(dataframe,loser_ID,'STREAK', "", 1)

    ratingW = datadriver.getUserValue(dataframe,winner_ID,'RANK')
    ratingL = datadriver.getUserValue(dataframe,loser_ID,'RANK')
    print(ratingW)
    print(ratingL)

    updatedW, updatedL = EloRating(ratingW,ratingL, 10, 1)

    print(updatedW)
    print(updatedL)

    datadriver.updateUserValue(dataframe,winner_ID,'RANK', updatedW)
    print(datadriver.getUserValue(dataframe,winner_ID,'RANK'))
    datadriver.updateUserValue(dataframe,loser_ID,'RANK', updatedL)
    print(datadriver.getUserValue(dataframe,loser_ID,'RANK'))

    print('value of wager indicator'.format(wager))

    if wager:
        winner_addy = datadriver.getUserValue(dataframe,winner_ID,'ETH_ADDY')
        print(winner_addy)
        loser_addy = datadriver.getUserValue(dataframe,loser_ID,'ETH_ADDY')
        print(loser_addy)

        #await asyncio.create_task(web3_logic.updateBalance(winner_addy,value,1))
        #await asyncio.create_task(web3_logic.updateBalance(loser_addy,value,1))
        #await asyncio.create_task(web3_logic.setRank(winner_addy,int(updatedW)))
        #await asyncio.create_task(web3_logic.setRank(winner_addy,int(updatedL)))
        #NOTE: web3_logic operations returns receipt. If status in response equals 1 the transaction was successful. If it is equals 0 the transaction was reverted by EVM
        await run_blocking(web3_logic.updateBalance,winner_addy,value,1)
        await run_blocking(web3_logic.setRank,winner_addy,int(updatedW))
        await asyncio.sleep(3)
        print(await run_blocking(web3_logic.updateBalance,loser_addy,value,0))
        await run_blocking(web3_logic.setRank,loser_addy,int(updatedL)) # Nonce too low


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)

    
#####################################################################
# Function: async def matchmaking(winner_ID, loser_ID)
# Parameters: 
#             
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: If initiated in local server, do not charge gas fee. Else, charge convience fee.
#####################################################################       

async def matchmaking(client, message):

    #GET RANKLIST

    #Find User in RANKLIST
    #while found == NONE -> search left and right of index for avaliable opponent.
    #If not found -> Return -1
    #Else initiate challenge() with found user.

    return

    
#####################################################################
# Function: async def stats(winner_ID, loser_ID)
# Parameters: winner_ID/loser_ID -> int discord user ID's
#             
# Behavior: 
#
# Returns:
# Author: Deanta Pittman
# Notes: implement pandas to mature file-based database ~ Replacing text files with csv file
#####################################################################
#displays the users total wins
async def stats(message):


    return


#Elo Rating Algorithm: Source: https://www.geeksforgeeks.org/elo-rating-algorithm/

# Function to calculate the Probability
def Probability(rating1, rating2):
  
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))
  

# Function to calculate Elo rating
# K is a constant.
# d determines whether
# Player A wins or Player B. 
def EloRating(Ra, Rb, K, d):
   
  
    # To calculate the Winning
    # Probability of Player B
    Pb = Probability(Ra, Rb)
  
    # To calculate the Winning
    # Probability of Player A
    Pa = Probability(Rb, Ra)
  
    # Case -1 When Player A wins
    # Updating the Elo Ratings
    if (d == 1) :
        Ra = Ra + K * (1 - Pa)
        Rb = Rb + K * (0 - Pb)
    # Case -2 When Player B wins
    # Updating the Elo Ratings
    else :
        Ra = Ra + K * (0 - Pa)
        Rb = Rb + K * (1 - Pb)
      
    
  
    print("Updated Ratings:-")
    print("Ra =", round(Ra, 6)," Rb =", round(Rb, 6))
    
    return Ra, Rb;









# MYSQL IMPLEMETATION of updaterecord(winner_ID, loser_id, game=0): NOTED FOR FUTURE REFERENCE
    #async def updaterecord(winner_str,loser_str, game = 0):
    #winner_str = winner_str
    #loser_str = loser_str
    #game = game
    #
    #conn = pyodbc.connect('Driver={SQL Server};'
    #                  'Server=msi\sqlexpress;'
    #                  'Database=dojobot_stats;'
    #                  'Trusted_Connection=yes;')
    #if loser_str != '0':
    #    #Updates win_count of winner user_name in localhost SQL Server
    #    cursor = conn.cursor()
    #    sql = "UPDATE datas SET win_count = (win_count + 1) WHERE CONVERT(VARCHAR, user_name) = (?);"
    #    val = (winner_str)
    #    cursor.execute(sql,val)
    #
    #if loser_str != '0':
    #    #Updates lose count with loser user_name in localhost SQL server
    #    sql = "UPDATE datas SET lose_count = (lose_count + 1) WHERE CONVERT(VARCHAR, user_name) = (?);"
    #    val = (loser_str)
    #    cursor.execute(sql,val)
    #
    #Updates challenge win
    #if game == 1:
    #    sql = "UPDATE datas SET challenge_wins = (challenge_win + 1) WHERE CONVERT(VARCHAR, user_name) = (?);"
    #    val = (winner_str)
    #    cursor.execute(sql,val)
    #   
    #conn.commit()

   #records.txtle’? y

# MYSQL IMPLEMENTATIOM FOR stats(message): SAVED FOR FUTURE REFERENCE
#    if message.mentions:
#        targeted_id = message.mentions[0].id
#    else:
#        targeted_id = message.author.id
#        
#    conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server=msi\sqlexpress01;'
#                      'Database=dojobot_stats;'
#                      'Trusted_Connection=yes;')
#    
#    cursor = conn.cursor()
#    sql = "SELECT win_count FROM datas WHERE user_id = (?);"
#    val = (targeted_id)
#    cursor.execute(sql,val)
#    wincount = cursor.fetchone()[0] #fetchone returns type tuple. First element is count
#    
#    sql = "SELECT lose_count FROM datas WHERE user_id = (?);"
#    val = (targeted_id)
#    cursor.execute(sql,val)
#    losecount = cursor.fetchone()[0]
#    
#    if losecount == 0:
#        ratio = 0
#   else:
#        ratio = int(wincount) / int(losecount)
#    
#    if message.mentions:
#        targeted_id = message.mentions[0].name
#    else:
#        targeted_id = message.author.name
#    
#    e = discord.Embed(title = str(targeted_id) + ' server stats', description = ' ')
#    e.add_field(name='Wins', value = wincount, inline = True)
#    e.add_field(name='Loses', value = losecount, inline = True)
#    e.add_field(name='W/L Ratio', value = ratio, inline = True)
#    
#    await message.channel.send(embed=e)

client.run(BOT_TOKEN)
