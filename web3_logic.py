import json
import math
import os
import time
import asyncio
import event_listener
import random
from dotenv import load_dotenv


load_dotenv()

#import infura
#from dotenv import load_dotenv
#from pycoingecko import CoinGeckoAPI
from solcx import compile_standard, install_solc
from web3 import Web3

COMMISSIONFEE = .03

#pool transactions? note nonce problem in race conditions.
#load_dotenv()

########################### ABI GENERATION ####################
with open("transaction.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.16")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"transaction.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.16",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["transaction.sol"]["Wager"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["transaction.sol"]["Wager"]["metadata"])["output"]["abi"]

###################### SMART CONTRACT CONNECTION CONFIG ############################
#web3 lib Python script
# MAINNET INFURA URL infura_url ="https://mainnet.infura.io/v3/af8778766a394b079160d1067fae3524"
infura_url= 'https://goerli.infura.io/v3/ad4ce9db8f4b404eada5374769188bae'  # GOERLI INFURA URL
chain_id = 5
my_address = '0xe5b957c7acC4d94006c75E3B5d6C07953B97b277'
PRIVATE_KEY= os.getenv('PRIVATE_KEY')
web3 = Web3(Web3.HTTPProvider(infura_url))
nonce = web3.eth.getTransactionCount(my_address)
print(web3.isConnected())

# Establish connection
CONTRACT_ADDY= os.getenv('CONTRACT_ADDY')
wager = web3.eth.contract(address=CONTRACT_ADDY, abi=abi)
# ----------------- Notes ---------------------------------------
#hash = web3.utils.sha3("Message to Sign");
#
# For connecting to ganache
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
# chain_id = 1337
# my_address = "0x7c84aEd4C270850B62b8D5Fe1186765dA988Ba32"
# private_key = "ef41ae096c96d4d296676e57899bc9c85d466bf59ddf981d0c03b8b996bcb7dc"

# Create the contract in Python
# Wager = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
# nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
#transaction = Wager.constructor().buildTransaction(
#    {
#        "chainId": chain_id,
#        "gasPrice": w3.eth.gas_price,
#        "from": my_address,
#        "nonce": nonce,
#    }
#)
# Sign the transaction
#signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#print("Deploying Contract!")
# Send it!
#tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
#print("Waiting for transaction to finish...")
#tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash) # ON INITIAL DEPLOYMENT, SAVE tx_receipt to file.
#print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# -------------------- CALL COMMANDS ----------------------

def getRank(ethAddy):
    return wager.functions.getRank(ethAddy).call()

# default value is Wei. Need to cast user input to GWei
def getBalance(ethAddy):
    return wager.functions.getBalance(ethAddy).call()

def isUser(ethAddy):
    return wager.functions.isUser(ethAddy).call()

def isPendingWithdraw(ethAddy):
    return wager.functions.isPendingWithdraw(ethAddy).call()


# ----------------- TRANSACTION COMMANDS --------------

#operation -> 0 = addition | 1 = subtraction
#value -> difference to apply to balance
def updateBalance(ethAddy,value,operation):
    print('wager value : {}'.format(value))

    if(operation): #Win State

        currentBalance = getBalance(ethAddy)
        print('Current Balance - In winner case {}'.format(currentBalance))
        afterfees = math.floor(value * (1 - COMMISSIONFEE)) # 3% COMMISSION FEE ON ALL WINNING TRANSACTIONS
        print('After Fees: {}'.format(afterfees))
        updatedBalance = currentBalance + afterfees

        transaction = wager.functions.setBalance(ethAddy,updatedBalance).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": web3.eth.gas_price,
                "from": my_address,
                "nonce": web3.eth.getTransactionCount(my_address),
            }
        )
        signed_greeting_txn = web3.eth.account.sign_transaction(
            transaction, private_key=PRIVATE_KEY
        )
        tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        
    else:

        currentBalance = getBalance(ethAddy)
        print('Current Balance - In loser case {}'.format(currentBalance))
        try:
            updatedBalance = currentBalance - value #NEED TO ENSURE NEVER NEGATIVE - RAISE ADMINERROR
            assert(updatedBalance > 0)
        except:
            return 0
        transaction = wager.functions.setBalance(ethAddy,updatedBalance).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": web3.eth.gas_price,
                "from": my_address,
                "nonce": web3.eth.getTransactionCount(my_address),
            }
        )
        signed_greeting_txn = web3.eth.account.sign_transaction(
            transaction, private_key=PRIVATE_KEY
        )
        tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)

    return tx_receipt


def setRank(ethAddy,elo):
    print('setRank elo: {}'.format(elo))
    transaction = wager.functions.setRank(ethAddy,elo).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": my_address,
            "nonce": web3.eth.getTransactionCount(my_address),
        }
    )
    signed_greeting_txn = web3.eth.account.sign_transaction(
        transaction, private_key=PRIVATE_KEY
    )
    tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)

    return tx_receipt

def addUser(ethAddy):
    print(nonce)
    transaction = wager.functions.addUser(ethAddy).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": my_address,
            "nonce": web3.eth.getTransactionCount(my_address)
        }
    )
    print(transaction)
    signed_greeting_txn = web3.eth.account.sign_transaction(
        transaction, private_key=PRIVATE_KEY
    )
    print(signed_greeting_txn)
    tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print(tx_greeting_hash)
    print("Updating stored Value...")

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash, timeout=120)
    print("value updated!")
    return tx_receipt

def initializeWithdraw(ethAddy, withdrawAmount):
    currentBalance = getBalance(ethAddy)
    assert(currentBalance > withdrawAmount) #need to create error handler
    transaction = wager.functions.initializeWithdraw(ethAddy,withdrawAmount).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": my_address,
            "nonce": web3.eth.getTransactionCount(my_address),
        }
    )
    signed_greeting_txn = web3.eth.account.sign_transaction(
        transaction, private_key=PRIVATE_KEY
    )
    tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print("Updating stored Value...")

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print("value updated!")
    return tx_receipt

##############################-------- EtherWatcher Element ---------##############################


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop\
# try to run the log_loop function above every 15 seconds

# FOR TESTING, call by command. Will need to implement channel placement. Will need to rewrite these functions in the future
initiate_filter = wager.events.userAdded.createFilter(fromBlock='latest')
withdraw_filter = wager.events.withdrawInitialized.createFilter(fromBlock='latest')
deposit_filter = wager.events.fundsAdded.createFilter(fromBlock='latest')
rank_filter = wager.events.rankUpdated.createFilter(fromBlock='latest')
balance_filter = wager.events.balanceUpdated.createFilter(fromBlock='latest')
async def pullWatcher():
  
    task = asyncio.create_task(event_listener.listen(initiate_filter,withdraw_filter,deposit_filter,rank_filter,balance_filter))
    #print("task initiated pullWatcher() - {}".format(task))
    await task
    #print("returning task pullWatcher() - {}".format(task))
    return task



#Used for testing local functions
if __name__ == "__main__":
    print(wager.all_functions())
    #addUser('0x7F1412c950807f4b964e9985868D57bD59DE9290')






























## ------------------------ LEGACY --------------------------------------

def getETHPrice():
    cg = CoinGeckoAPI()
    ether_price = cg.get_price(ids='ethereum', vs_currencies='usd')
    print(ether_price)
    ether_value = ether_price['ethereum']
    ether_usd = ether_value['usd']
    return ether_usd


def sendTransaction(ether_usd, user_addy, user_balance):
    transaction_total = user_balance / ether_usd
    print(ether_usd)
    nonce = web3.eth.getTransactionCount(source_account)
    tx = {
        'nonce': nonce,
        'to': user_addy,
        'value': web3.toWei(transaction_total, 'ether'),
        'gas': 100000 ,
        'gasPrice': web3.eth.gas_price
        }
    signed_tx = web3.eth.account.signTransaction(tx,PRIVATE_KEY)
    print("signed transaction")
    tx_rawhash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("transaction out")
    tx_hash = web3.toHex(tx_rawhash)
    return tx_hash

def waitReceipt(tx_hash):
    
    received = 0
    while not received:
        try:
            web3.eth.get_transaction(tx_hash)
            print('receive')
            received = 1
        except:
            print('hold')
            time.sleep(1)
