#Ethereum Event Listener Tutorial: https://cryptomarketpool.com/how-to-listen-for-ethereum-events-using-web3-in-python/
import json
from queue import Empty
from web3 import Web3
import asyncio
import os
import time

from dotenv import load_dotenv

load_dotenv()

#from pycoingecko import CoinGeckoAPI
from solcx import compile_standard, install_solc
from web3 import Web3


#load_dotenv()


with open('transaction.sol', 'r') as file:
    simple_storage_file = file.read()

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
abi = json.loads(
    compiled_sol["contracts"]["transaction.sol"]["Wager"]["metadata"]
    )["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# web3 lib Python script
# MAINNET INFURA URL infura_url ="https://mainnet.infura.io/v3/af8778766a394b079160d1067fae3524"
infura_url = "https://goerli.infura.io/v3/ad4ce9db8f4b404eada5374769188bae"  # Goerli INFURA URL
w3 = Web3(Web3.HTTPProvider(infura_url))
#print(web3.isConnected())

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


# Working with deployed Contracts
contract_addy= os.getenv('CONTRACT_ADDY')
contract = w3.eth.contract(address=contract_addy, abi=abi)
# add your blockchain connection information

# contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)

# define function to handle events and print to the console

# https://www.w3schools.com/python/python_json.asp
def handle_event(event_type, event):
    extractedArguments = []
    print("{} event caught! Decoding".format(event_type))
    jsonobj = Web3.toJSON(event)
    eventdata = json.loads(jsonobj)
    #print(eventdata)

    for data in eventdata:
        if(event_type == 'addUser'):   
            extractedArguments.append(data['args']['userAddy'])

        if(event_type == 'withdrawFunds'):
            extractedArguments.append(data['args']['userAddy'])
            extractedArguments.append(data['args']['withdrawl'])
            extractedArguments.append(data['args']['updatedUserBalance'])
            #
        if(event_type == 'depositFunds'):
            extractedArguments.append(data['args']['userAddy'])
            extractedArguments.append(data['args']['depositAmount'])
            extractedArguments.append(data['args']['updatedBalance'])
        if(event_type == 'rankUpdated'):
            extractedArguments.append(data['args']['userAddy'])
            extractedArguments.append(data['args']['rank'])
            
        if(event_type == 'balanceUpdated'):
            extractedArguments.append(data['args']['userAddy'])
            extractedArguments.append(data['args']['balance'])
            
    
    #print("returning extractedArgument - {} ".format(extractedArguments))
    return extractedArguments

     # pass data and event_type to function in ultimate.py to post in channel and update local database 


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_type, event_filter, poll_interval):
    eventLog = []
    #print("listening...")
    try:
        newEvents = event_filter.get_new_entries()
    except:
        print('error')
    #print(newEvents)
    if newEvents:
        event = handle_event(event_type, newEvents)
        #print(event)
        eventLog.append(event)
    #else:
    #    print("No new Events: {}".format(newEvents))
    
    #print("returning eventLog {0} - {1} ".format(event_type, eventLog))
    return eventLog


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop\
# try to run the log_loop function above every 2 seconds
async def listen(initiate_filter,withdraw_filter,deposit_filter,rank_filter,balance_filter):
    addUser_log = [] 
    withdrawFunds_log = []
    depositFunds_log = []
    rankUpdated_log = []
    balanceUpdated_log = []

    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    #while True:
    loop = asyncio.get_event_loop()
    try:
    #    print('loop initiated')
        
        addUser_log, withdrawFunds_log, depositFunds_log, rankUpdated_log, balanceUpdated_log = await asyncio.gather(
                log_loop('addUser', initiate_filter, 10),
                log_loop('withdrawFunds',withdraw_filter, 10),
                log_loop('depositFunds',deposit_filter, 10),
                log_loop('rankUpdated',rank_filter, 10),
                log_loop('balanceUpdated',balance_filter, 10),
                )
        print(addUser_log)
    #    print('loop complete - returned logs below')
    except: ('error: gatherloop')

    finally:
        # close loop to free up system resources
        # return addUser_log, withdrawFunds_log, depositFunds_log
    #    print('returning listen() addUser - {0} | withdrawFunds - {1} | depositFunds - {2}'.format(addUser_log,withdrawFunds_log,depositFunds_log))
        return addUser_log, withdrawFunds_log, depositFunds_log, rankUpdated_log, balanceUpdated_log

#if __name__ == "__main__":
        #main()