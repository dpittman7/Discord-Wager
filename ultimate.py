import discord
from discord import app_commands
import math
from random import shuffle, randint  
from datetime import datetime
from discord.ui import Button, View
from discord.ext import commands
import web3_logic
import functools
import typing
import asyncio
import requests
import os
from dotenv import load_dotenv
from utilities import datadriver

load_dotenv()
MY_GUILD = discord.Object(id=701644736901021736)



class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)
    
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
client = MyClient(intents=intents)
reaction = discord.Reaction

ETHERSCAN_TOKEN= os.getenv('ETHERSCAN_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CURRENT_CONTRACT = os.getenv('CONTRACT_ADDY')
POLL_INTERVAL = 30
RANK_THRESHOLD = 100
#RANKLIST = treeSet.TreeSet()
FILENAME = os.getenv('FILENAME')
#dataframe = datadriver.loadTable(FILENAME)

@client.event
async def on_ready():
    guild_list = client.guilds #sees all the users that the bot can see.

    #guild = discord.utils.find(lambda m: m.guild == 'Ultimate', guild_list)
    #active_role = discord.utils.find(lambda m: m.role == 'Active', guild.roles)
    #active_members = active_role.members

    #dataframe = datadriver.loadTable(FILENAME)
    #spliceframe = dataframe.iloc[:,[0,5]] #creates dataframe with only USERNAME and RANK as columns. Still row indexed by ID
    #print(spliceframe)

    

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

#@client.tree.command()
#async def buttontester(interaction: discord.Interaction, member: discord.Member):
#    print(interaction.expires_at)
#
#    #Build Embed to be sent
#    e = discord.Embed(title = 'Button Debugger')
#    
#    #Build buttons 
#    button_one = Button(label="Button One toggled")
#    button_two = Button(label="Button Two toggled")
#
#    view = View(timeout = 600)
#    view.add_item(button_one)
#    view.add_item(button_two)
#
#    #Send Initial Response
#    og_response = await interaction.response.send_message(embed=e, view=view)
#    print(og_response)
#    #await og_response.defer()
#
#    print("indicatior 1")
#    win_status = [0,0]
#    confirm_status = [0,0]
#
#    async def button_one_callback(interaction):
#        print('interaction received')
#        #assign check confirming button user is correct
#        
#        #if button two has not toggled - initial win
#        if win_status[1] == 0:
#            win_status[0] = 1
#            button_one.disabled = True
#            e.add_field(name='button_one toggled - pending button_two', value=1, inline = False)
#            await interaction.edit_original_response(embed=e, view=view)
#
#        #if button two is toggled - claiming win
#        if win_status[1] == 1:
#            confirm_status[0] = 1
#            button_one.disabled = True
#            e.add_field(name='button_one toggled - confirmed button_two toggle', value=1, inline = False)
#            await interaction.edit_original_response(embed=e, view=view)
#
#    
#    async def button_two_callback(interaction):
#        print('interaction received')
#        #assign check confirming button user is correct
#        
#        #if button one has not toggled - initial win
#        if win_status[0] == 0:
#            win_status[1] = 1
#            button_one.disabled = True
#            e.add_field(name='button_one toggled - pending button_two', value=1, inline = False)
#            await interaction.edit_original_response(embed=e, view=view)
#
#        #if button two is toggled - claiming win
#        if win_status[0] == 1:
#            confirm_status[1] = 1
#            button_one.disabled = True
#            e.add_field(name='button_one toggled - confirmed button_two toggle', value=1, inline = False)
#            await interaction.edit_original_response(embed=e, view=view)
#    
#    async def status_check(interaction, win_status, confirm_status):
#        concluded = 0
#        
#        if win_status[0] == 1 and confirm_status[1] == 1:
#            e.add_field(name='button_one win - end interaction', value=1, inline = False)
#            concluded = 1
#            #await interaction.edit_original_response(embed=e, view=view)
#        
#        if win_status[1] == 1 and confirm_status[0] == 1:
#            e.add_field(name='button_two win - end interaction', value=1, inline = False)
#            concluded = 1
#            #await interaction.edit_original_response(embed=e, view=view)
#        return concluded
#            
#
#
#
#    #Enter incomplete state
#    
#    finished = 0
#    print("in indicatior loop")
#    while(not finished):
#        button_one.callback = button_one_callback
#        button_two.callback = button_two_callback
#        finished = await status_check(interaction,win_status,confirm_status)
        


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

                                                                                                                                                                                                                                                           

#####################################################################
# Function: contractLogger(discord.channel)
# Parameters: channel - 
#
# Behavior: represents channel in server where contract-events are
#           to be posted.
#
# Returns: -
# Author: Deanta Pittman
# Notes: All events are logged in nohup.out in prod. Consider creating logging system.
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
        e = discord.Embed(title = 'Contract Event Emit', description='Credit Deposit', url = 'https://goerli.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
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
        e = discord.Embed(title = 'Contract Event Emit', description='User Rank Updated', url = 'https://goerli.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Current Rank', value='{}'.format(rank), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        await channel.send(embed=e)


        print(addy)
        print(rank)
       
    
    for addy, balance in balanceUpdated_log:

        print("inside Embed Formation")
        e = discord.Embed(title = 'Contract Event Emit', description='User Balance Updated', url = 'https://goerli.etherscan.io/address/{}#events'.format(CURRENT_CONTRACT))
        e.add_field(name='User Address', value=addy, inline = False)
        e.add_field(name='Current Balance', value='{} Wei'.format(balance), inline = True)
        e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
        await channel.send(embed=e)


        print(addy)
        print(balance)
        

    #print("returning task contractLogger() - {}".format(result.result()))
         
        

########################################################################
# Function: login(discord.interaction)
# Parameters: interaction - SLASH COMMAND
#
# Behavior: Discord facing status / grants user role 'Active' in server.
#
# Returns:
# Author: Deanta Pittman
# Notes: Add database interaction to be able to reflect status on website
#########################################################################
@client.tree.command()
async def login(interaction: discord.Interaction):
    user = interaction.user

    #ADD: Check if the user has role "In Match" - Send Error Message and terminate function.
    if datadriver.getUserValue(user.id, 'IN_CHALLENGE'):
        interaction.response.send_message("Complete current challenge before changing status.")
    else:    
        role = discord.utils.get(client.guilds[0].roles, name="Active")
        await user.add_roles(role)
        
        role = discord.utils.get(client.guilds[0].roles, name="Inactive")
        await user.remove_roles(role)


########################################################################
# Function: logout(discord.interaction)
# Parameters: interaction - SLASH COMMAND
#
# Behavior: Discord facing status / grants user role 'InActive' in server.
#
# Returns:
# Author: Deanta Pittman
# Notes: Add database interaction to be able to reflect status on website
#########################################################################

#will need to add timeout when launched onto external server    
@client.tree.command()
async def logout(interaction: discord.Interaction):
    user = interaction.user

    #ADD: Check if the user has role "In Match" - Send Error Message and terminate function.
    if datadriver.getUserValue(user.id, 'IN_CHALLENGE'):
        interaction.response.send_message("Complete current challenge before changing status.")
    else:
        role = discord.utils.get(client.guilds[0].roles, name="Inactive")
        await user.add_roles(role)
        
        role = discord.utils.get(client.guilds[0].roles, name="Active")
        await user.remove_roles(role)

#####################################################################
# Function: toggleInChallenge(userID,toggle)
# Parameters: toggle - control parameter to determine which state to 
#                      toggle to.
#
# Behavior: InChallenge must be false to initiate new challenges
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################
def toggleInChallenge(userID, toggle):
    #df = datadriver.loadTable(FILENAME)
    datadriver.updateUserValue(userID,'IN_CHALLENGE',toggle)
    

#####################################################################
# Function: getRank(discord.interaction)
# Parameters: interaction - SLASH COMMAND
#
# Behavior: Retreives message sender rank from server database
#
# Returns:
# Author: Deanta Pittman
#
# Notes: To further decentralize, consider to call web3 value directly.
#        Server mirrors Contract Values. CQRS style database segregation.
#####################################################################   
@client.tree.command()
async def getrank(interaction: discord.Interaction):
    #dataframe = datadriver.loadTable(FILENAME)
    rank = datadriver.getUserValue(interaction.user.id,'ranking')
    await interaction.response.send_message('Current Rank: {}'.format(rank))

#####################################################################
# Function: getbalance(interaction, member)
# Parameters: interaction - SLASH COMMAND
#             member - discord.member -> used to access member.id to 
#                                        retreive ETH addy.
#
# Behavior: Retreives block value of balance
#
# Returns:
# Author: Deanta Pittman
#
# Notes: Balance must always be validated by contract to 
#        avoid any possible race conditions.
#####################################################################  

@client.tree.command()
async def getbalance(interaction: discord.Interaction, member: discord.Member):
    #dataframe = datadriver.loadTable(FILENAME)
    addy = datadriver.getUserValue(member.id,'ETH_ADDY')
    print("returned addy: {}".format(addy))
    if web3_logic.isUser(addy):
        balance = web3_logic.getBalance(addy)
        await interaction.response.send_message('Current Balance: {}'.format(balance))
    else:
        await interaction.response.send_message('User is not currently registered in contract.')   

#####################################################################
# Function: initializeuser
# Parameters: interaction -> SLASH COMMAND
#             ethaddress -> ethereum address to be added to contract.
#             profilepic -> to be downloaded to server, uploaded to imgur, and link stored.
#
# Behavior: initalizes the user (duh.) adds user to local database and to 
#           ethereum smart contract. error handling applied at module.
#           
#
# Returns: None - returns error status for interaction
# Author: Deanta Pittman
#
# Notes: Need to validate passed ETH addy and error handling to datadriver class
#####################################################################  

@client.tree.command()
async def initializeuser(interaction: discord.Interaction, ethaddress: str, profilepic: discord.Attachment):
        filename = "{}_pfp".format(interaction.user.id)
        await profilepic.save("profilepics/{}.png".format(filename))
        #Need to add logic to validate user inputted address
        errors = []
        sqlerror = datadriver.addUser(interaction.user.id,interaction.user.name,ethaddress,filename)
        if sqlerror:
            errors.append(sqlerror)

        web3error = web3_logic.addUser(ethaddress)
        if web3error:
            errors.append(web3error)
        
        if errors:
            await interaction.response.send_message('Following errors occured: {}'.format(errors))
        else:
            await interaction.response.send_message('User added, welcome to the mix {}!'.format(interaction.user.name))

        
#add rank difference to eligible function
#gamelist[0] - initiatorID , gamelist[1] = opponentID
#####################################################################
# Function:
# Parameters:
#
# Behavior: Internal function
#
# Returns:
# Author: Deanta Pittman
#
# Notes: Implement questioning in user DM's
#####################################################################
async def eligible(gamelist,wagerValue):
    eligible = 0
    #dataframe = datadriver.loadTable(FILENAME)
    try:
        initiatorAddy = datadriver.getUserValue(gamelist[0],'ETH_ADDY')
        opponentAddy = datadriver.getUserValue(gamelist[0],'ETH_ADDY')
        if initiatorAddy != "" and initiatorAddy != "":
            print("evaluating web3 stats")
            balance1 = web3_logic.getBalance(initiatorAddy) 
            balance2 = web3_logic.getBalance(opponentAddy)
            print(" User Balances - {0} | {1}".format(balance1,balance2))

            rank1 = web3_logic.getRank(initiatorAddy)
            rank2 = web3_logic.getRank(opponentAddy)
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


async def selectWager(message,gamelist, initiatorData, opponentData):
    

    r = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey={}'.format(ETHERSCAN_TOKEN)) #Etherscan API
    ethprice = float(r.json()["result"]["ethusd"])
    print(ethprice)
    e = discord.Embed(title = 'Select Wager Amount', color=discord.Color.yellow())
    e.add_field(name='.001 Ether', value='~ {} USD'.format(ethprice*.001), inline = True)
    e.add_field(name='.003 Ether', value='~ {} USD'.format(ethprice*.003), inline = True)
    e.add_field(name='.005 Ether', value='~ {} USD'.format(ethprice*.005), inline = True)
    e.add_field(name='{} Selection'.format(initiatorData[0]), value='X', inline = False)
    e.add_field(name='{} Selection'.format(opponentData[0]), value='X', inline = False)
    e.set_footer(text='React to choose your selection', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
    activeEmbed = await message.edit(embed=e)

    await activeEmbed.add_reaction(str('1️⃣')) #unicode for 100 points
    await activeEmbed.add_reaction(str('3️⃣')) #unicode for cross mark
    await activeEmbed.add_reaction(str('5️⃣')) #unicode for cross mark
    value = 0
    selection = 0
    initiatorsChoice = -1
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
            e.set_field_at(index=3,name='{}'.format(initiatorData[0]),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 1
            
            
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=3,name='{}'.format(initiatorData[0]),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 3

        if reactorID == gamelist[0] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=3,name='{}'.format(initiatorData[0]),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 5

        #Evaluating Opposition Choice 
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('1️⃣'):
            e.set_field_at(index=4,name='{}'.format(opponentData[0]),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 1
            
            
        if reactorID == gamelist[1] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=4,name='{}'.format(opponentData[0]),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 3

        if reactorID == gamelist[1] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=4,name='{}'.format(opponentData[0]),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            oppositionsChoice = 5

        await asyncio.sleep(1)
        print('{0} - {1}'.format(initiatorsChoice,oppositionsChoice))

        if oppositionsChoice == initiatorsChoice:
            e = discord.Embed(title = 'Wager Amount Selected', color=discord.Color.green())
            e.add_field(name='.00{} Ether'.format(oppositionsChoice), value='approx {} USD'.format(ethprice*.001), inline = True)
            e.set_footer(text='The wager will begin shortly.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
            activeEmbed = await activeEmbed.edit(embed=e)
            await activeEmbed.delete(delay=5.0)
            value = oppositionsChoice * 1000000000000000
            selection = 1
    
    return value


#####################################################################
# Function: challenge(interaction, opponent, wager)
# Parameters: interaction -> SLASH COMMAND
#             opponent -> to retreive opponents id.
#             wager -> to toggle a wager match or not.
#
# Behavior: To initate a challenge between two users.
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

@client.tree.command()
async def challenge(interaction: discord.Interaction, opponent: discord.Member, wager: bool):
    

    # dataframe = datadriver.loadTable(FILENAME)
    initiator = interaction.user
    await interaction.response.defer()
    
    #Declarations
    gamelist = [] #gamelist[0] - initiatorID , gamelist[1] = opponentID
    status_state = [0,0,0,0,0] #game[0] - state. game[1] - gamecount, game[2] - win state, game[3] -initiator_wincount, game[4] - opponent_wincount
    date = datetime.date #date object to get date of posting the embed
    value = 0
    gamelist, initiatorData, oppositionData = await initialize([initiator.id,opponent.id])

    #check if any member is currently in active challenge
    if(datadriver.getUserValue(opponent.id,'IN_CHALLENGE') or 
       datadriver.getUserValue(initiator.id,'IN_CHALLENGE')):
        print(datadriver.getUserRow(opponent.id))
        print(datadriver.getUserRow(initiator.id))
        await interaction.followup.send(content="complete current challenge")
        return
    

    if(wager):
        value = await selectWager(interaction,gamelist, initiatorData, oppositionData)
        if not await eligible(gamelist, value):
            await interaction.followup.send(content="A user is unelgible for wager matches, ensure all parties meet the requirements defined in #how-to-use")
            await asyncio.sleep(5)
            status_state[0] = -1
    else:
        message = await interaction.followup.send("Challenge initiated")
    
    toggleInChallenge(initiator.id,1)
    toggleInChallenge(opponent.id,1)
    
    
    print(0)
    #initiate challenge
    
    #print(gamelist[1])
    if status_state[0] == 0:  status_state, activeEmbed = await confirm(client, message, gamelist, status_state, reaction, wager, value)
    print(status_state[0])
    if status_state[0] == 2: await gamecount(client, status_state, gamelist, activeEmbed)
    while (status_state[0] == 3 or status_state[0] == 4):
        if status_state[0] == 3: await inprogress(client,gamelist, status_state, wager, value,activeEmbed)
        if status_state[0] == 4: await postresult(client,gamelist, status_state, date, wager, value)
        await message.edit(content="Challenge complete, gg.")


    if status_state[0] == -1 :
        await message.edit(content="Challenge Terminated")
        await message.delete(delay=5.0)
        


#####################################################################
# Function: confirm(client, message, gamelist, status_state, reaction, wager, value)
# Parameters: client ->
#             message -> 
#             gamelist -> 
#             status_state
#             reaction ->
#             wager ->
#             value ->
#
# Behavior: confirmation prompt, opponent selects reaction to continue the script.
#
# Returns: 
# Author: Deanta Pittman
# Notes: 
#####################################################################
    
async def confirm(client, message, gamelist, status_state, reaction, wager = 0, value = 0):
    #confirm challenge
    gamelist, initiatorStats, oppositionStats = await initialize(gamelist)
    print('gamelist {}'.format(*gamelist))
    status_state[0] = 1


    #Create Embed 
    e = discord.Embed(title = 'Challenge', color=discord.Color.yellow())
    e.add_field(name='CHALLENGER', value=initiatorStats[0], inline = False)
    e.add_field(name='RANK', value=initiatorStats[1], inline = True)
    e.add_field(name='WINS', value=initiatorStats[2], inline = True)
    e.add_field(name='STREAK', value=initiatorStats[3], inline = True)
    e.add_field(name='vs', value=" --- pending --- ", inline = False)
    e.add_field(name='OPPOSITION', value=oppositionStats[0], inline = False)
    e.add_field(name='RANK', value=oppositionStats[1], inline = True) 
    e.add_field(name='WINS', value=oppositionStats[2], inline = True)
    e.add_field(name='STREAK', value=oppositionStats[3], inline = True)
    if wager:
        e.add_field(name='WAGER VALUE', value=value, inline = False)
    e.set_footer(text='The Messenger Brings News', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')

    
    challengeEmbed = await message.edit(embed=e)
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
            #await message.channel.send('The initiator arives, welcome.'.format(gamelist[0]))
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
            status_state[0] = await terminate(gamelist) 

    await asyncio.sleep(3)
    return status_state, challengeEmbed    
    

#####################################################################
# Function:
# Parameters: client ->
#             interaction -> 
#             gamelist -> 
#             status_state
#             reaction ->
#             wager ->
#             value ->
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def gamecount(client, status_state, gamelist, activeEmbed): #strip gamecount.
    #state gamecount
    print(5)
    #print(status_state[0])
    gamelist, initiatorStats, oppositionStats = await initialize(gamelist)

    initiatorsChoice = 855
    oppositionsChoice = 100
    abort = 0
    e = discord.Embed(title = 'Select GameCount', color=discord.Color.yellow())
    e.add_field(name='{}'.format(initiatorStats[0]), value='X', inline = True)
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
            e.set_field_at(index=0,name='{}'.format(initiatorStats[0]),value="1")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 1
            
            
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('3️⃣'):
            e.set_field_at(index=0,name='{}'.format(initiatorStats[0]),value="3")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 3

        if reactorID == gamelist[0] and str(reactEvent[0]) == str('5️⃣'):
            e.set_field_at(index=0,name='{}'.format(initiatorStats[0]),value="5")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = 5
        
        if reactorID == gamelist[0] and str(reactEvent[0]) == str('❌'):
            e.set_field_at(index=0,name='{}'.format(initiatorStats[0]),value="ABORTED")
            activeEmbed = await activeEmbed.edit(embed=e)
            initiatorsChoice = -1

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
        print('{0} - {1}'.format(initiatorsChoice,oppositionsChoice))

        if oppositionsChoice == -1 or initiatorsChoice == -1:
            abort = 1
            await activeEmbed.delete(delay=7.0)
            status_state[0] = await terminate(gamelist,message)



        if oppositionsChoice == initiatorsChoice and not abort:

            e = discord.Embed(title = 'Challenge:', color=discord.Color.green())
            e.add_field(name='CHALLENGER', value=initiatorStats[0], inline = False)
            e.add_field(name='RANK', value=initiatorStats[1], inline = True)
            e.add_field(name='WINS', value=initiatorStats[2], inline = True)
            e.add_field(name='STREAK', value=initiatorStats[3], inline = True)
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
# Function: inprogress(client, message, gamelist,status_state,wager,value,activeEmbed )
# Parameters: client ->
#             interaction -> 
#             gamelist -> 
#             status_state
#             reaction ->
#             wager ->
#             value -> 
#
# Behavior:
#
# Returns:
# Author: Deanta Pittman
# Notes: 
#####################################################################

async def inprogress(client,gamelist,status_state,wager = 0 , value = 0, activeEmbed=discord.message):
    gamelist, initiatorStats, oppositionStats = await initialize(gamelist)
    initiator_ID = gamelist[0]
    opposition_ID = gamelist[1]
    print(initiator_ID)
    print(opposition_ID)
    print(status_state)
    
    
    initiator_name = initiatorStats[0]
    opponent_name = oppositionStats[0]

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
            e = discord.Embed(title = 'Challenge: {0} vs {1}'.format(initiatorStats[0],oppositionStats[0]))
            e.add_field(name= 'Game Number', value=(games + 1), inline=False)
            e.add_field(name=initiator_name, value = status_state[3], inline = True)
            e.add_field(name=opponent_name, value = status_state[4], inline = True)
            e.set_footer(text='Winner Selects Reaction.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')

            await activeEmbed.edit(embed = e)
            

            
            #response can only be done once
            
            game_state = [0,0]
            game_confirm = 0

            await activeEmbed.add_reaction(str('1️⃣')) #unicode for 100 points
            
            while not game_confirm:
                

                #Await users to play game and winner adds reaction
                reactEvent = await client.wait_for('reaction_add')
                reaction = reactEvent[0]
                print(reaction) #Reaction Object of awaited react event
                reactorID = reactEvent[1].id # ID of reactor
                print(reactorID)
                print(game_state)


                #Initiator gets inital reaction -> Prompt for confirmation
                if reactorID == initiator_ID and str(reactEvent[0]) == str('1️⃣'):
                    #Initiator claiming win
                    if(game_state[0] == 0 and game_state[1] == 0):
                        e.set_field_at(index=2,name='{}'.format(oppositionStats[0]),value="confirm?")
                        e.set_footer(text='Loser confirm by selecting reaction.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
                        await activeEmbed.edit(embed=e)
                        await activeEmbed.clear_reaction(str('1️⃣')) #unicode for 100 points
                        await activeEmbed.add_reaction(str('👍')) #unicode for cross mark
                        game_state[0] = 1
                
                #Initiator confirming reaction -> 
                if reactorID == initiator_ID and str(reactEvent[0]) == str('👍'):
                    print("confirm check 1")
                    print(game_state)
                    #Initiator confirming win
                    if(game_state[0] == 0 and game_state[1] == 1):
                        print("initiator confirming win")
                        e.set_field_at(index=2,name='{}'.format(oppositionStats[0]),value="win claimed.")
                        await activeEmbed.edit(embed=e)
                        status_state[4] += 1
                        await updaterecord(initiator_ID,opposition_ID)
                        game_state = [0,0]
                        await activeEmbed.clear_reaction(str('👍')) #unicode for 100 points
                        game_confirm = 1
                


                #Opponent gets inital reaction -> Prompt for confirmation
                if reactorID == opposition_ID and str(reactEvent[0]) == str('1️⃣'):
                    #Opposition claiming win
                    if(game_state[0] == 0 and game_state[1] == 0):
                        e.set_field_at(index=1,name='{}'.format(initiatorStats[0]),value="confirm?")
                        e.set_footer(text='Loser confirm by selecting reaction.', icon_url='https://lastfm.freetls.fastly.net/i/u/770x0/73ada0c9f3d8cfe35e64a37502c369a3.jpg#73ada0c9f3d8cfe35e64a37502c369a3')
                        activeEmbed = await activeEmbed.edit(embed=e)
                        await activeEmbed.clear_reaction(str('1️⃣')) #unicode for 100 points
                        await activeEmbed.add_reaction(str('👍')) #unicode for cross mark
                        game_state[1] = 1
                
                if reactorID == opposition_ID and str(reactEvent[0]) == str('👍'):
                    print("confirm check 2")
                    print(game_state)
                    #Initiator confirming win
                    if(game_state[0] == 1 and game_state[1] == 0):
                        print("opposition confirming win")
                        e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="win claimed.")
                        await activeEmbed.edit(embed=e)
                        status_state[3] += 1
                        await updaterecord(initiator_ID,opposition_ID)
                        await activeEmbed.clear_reaction(str('👍'))
                        game_state = [0,0]
                        game_confirm = 1

                if game_confirm:
                    await asyncio.sleep(3)
                    e.set_field_at(index=1,name='{}'.format(oppositionStats[0]),value="next round loading.")
                    e.set_field_at(index=2,name='{}'.format(oppositionStats[0]),value="gl.")
                    await activeEmbed.edit(embed=e)
                    asyncio.sleep(3)


                    

        
            if status_state[3] == wontheSet or status_state[4] == wontheSet:
                concluded = 1
                await activeEmbed.channel.send('Game match reached! Winner is decided')
           
            if status_state[3] == wontheSet:
                await updaterecord(initiator_ID,opposition_ID, wager, value) #When status state 3 == status state 2, initiator has won.
            if status_state[4] == wontheSet:
                await updaterecord(opposition_ID,initiator_ID, wager, value)
    
    if abort:
        status_state[0] = await terminate(gamelist)
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

async def postresult(client,gamelist,status_state,date, wager = 0, value = 0):
    print('posting results in message channel')

    gamelist, initiatorStats, oppositionStats = await initialize(gamelist)

    #dataframe = datadriver.loadTable(FILENAME)
    initiator_name = initiatorStats[0]
    opponent_name = oppositionStats[0]
    initiator_rank = datadriver.getUserValue(gamelist[0],'ranking')
    opponent_rank = datadriver.getUserValue(gamelist[1],'ranking')
    time = datetime.now()
    
    e = discord.Embed(title = 'Challenge Results: ' + initiator_name + ' vs ' + opponent_name, description = 'Best of ' + str(status_state[1]))
    e.set_footer(text= 'Time of completion: ' + str(time) )
    e.add_field(name='{0} - {1}'.format(initiator_name, initiator_rank), value = status_state[3], inline = True)
    e.add_field(name='{0} - {1}'.format(opponent_name, opponent_rank), value = status_state[4], inline = True)
    
    channel = client.get_channel(861363885747470337)
    await channel.send(embed=e)

    datadriver.updateUserValue(gamelist[0],'IN_CHALLENGE',0)
    datadriver.updateUserValue(gamelist[1],'IN_CHALLENGE',0)
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

async def initialize(affiliatedIDs):
    #inital message will determine playerlist
    playerlist = []
    initiatorID = affiliatedIDs[0]
    opponentID = affiliatedIDs[1]
    playerlist.append(initiatorID)
    playerlist.append(opponentID)
    

    #dataframe = datadriver.loadTable(FILENAME)
    initiatorStats = []
    initiatorStats.append(datadriver.getUserValue(playerlist[0],'USERNAME'))
    initiatorStats.append(datadriver.getUserValue(playerlist[0],'ranking'))
    initiatorStats.append(datadriver.getUserValue(playerlist[0],'WINS'))
    initiatorStats.append(datadriver.getUserValue(playerlist[0],'STREAK'))

    oppositionStats = []
    oppositionStats.append(datadriver.getUserValue(playerlist[1],'USERNAME'))
    oppositionStats.append(datadriver.getUserValue(playerlist[1],'ranking'))
    oppositionStats.append(datadriver.getUserValue(playerlist[1],'WINS'))
    oppositionStats.append(datadriver.getUserValue(playerlist[1],'STREAK'))

    #SETS IN_CHALLENGE TO 1, USED IN NEGATING USERS CALLING OTHER COMMANDS WHILE IN CHALLENGE
    #toggleInChallenge(initiatorID,1)
    #toggleInChallenge(opponentID,1)


    return playerlist, initiatorStats, oppositionStats
    

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
 
async def update_state(status_state,state=0, gamecount=0,winstate=0,initiator_wincount = 0, opponent_wincount = 0):
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
    if initiator_wincount != 0 :
        status_state[3] += 1
    if opponent_wincount != 0 :
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

async def terminate(gamelist):
    toggleInChallenge(gamelist[0],0)
    toggleInChallenge(gamelist[1],0)
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

    #dataframe = datadriver.loadTable(FILENAME)
    datadriver.updateUserValue(winner_ID,'WINS')
    datadriver.updateUserValue(loser_ID,'LOSES')

    datadriver.updateUserValue(winner_ID,'TOTAL')
    datadriver.updateUserValue(loser_ID,'TOTAL')

    datadriver.updateUserValue(winner_ID,'STREAK')
    datadriver.updateUserValue(loser_ID,'STREAK', "", 1)

    ratingW = int(float(datadriver.getUserValue(winner_ID,'ranking')))
    ratingL = int(float(datadriver.getUserValue(loser_ID,'ranking')))
    print(ratingW)
    print(ratingL)

    updatedW, updatedL = EloRating(ratingW,ratingL, 10, 1)

    print(updatedW)
    print(updatedL)


    print('value of wager indicator'.format(wager))

    if wager:
        winner_addy = datadriver.getUserValue(winner_ID,'ETH_ADDY')
        print(winner_addy)
        loser_addy = datadriver.getUserValue(loser_ID,'ETH_ADDY')
        print(loser_addy)

        datadriver.updateUserValue(winner_ID,'ranking', updatedW)
        print(datadriver.getUserValue(winner_ID,'ranking'))
        datadriver.updateUserValue(loser_ID,'ranking', updatedL)
        print(datadriver.getUserValue(loser_ID,'ranking'))

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



client.run(BOT_TOKEN)
