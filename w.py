#import libraries and classes
import subprocess #calls the ./derive script from python
import json
from dotenv import load_dotenv
import os
from web3 import Web3
from bit import *
from eth_account import Account

from constants import *

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#load EV
load_dotenv()

#get the mnemonic .env
mnemonic = os.getenv('mnemonic')



def derive_wallets(mnemonic, coin, numderive):
    
    command = f'php ./hd-wallet-derive.php -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' 
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()
    print(output)
    keys = json.loads(output)
    return  keys


coins = {"eth", "btc-test", "btc"}
numderive = 3

eth_privatekey = coins['eth'][0]['privkey']
btc_privatekey = coins['btc-test'][0]['privkey']
print(json.dumps(eth_privateKey, indent=4, sort_keys=True))
print(json.dumps(btc_privateKey, indent=4, sort_keys=True))
print(json.dumps(keys, indent=4, sort_keys=True))

    
def priv_key_to_account(coin, priv_key):
   
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    
eth_acc = priv_key_to_account(ETH,eth_PrivateKey)
btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)

    
eth_account = priv_key_to_account(ETH,eth_pk)

btc_account = priv_key_to_account(BTCTEST,btc_pk)

def create_tx(coin,account,recipient,amount):
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
        
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])  

def send_tx (coin, account, recipient, amount):
    if coin =='ETH':
        trxns_eth = create_tx(coin,account, recipient, amount)
        sign_trxns_eth = account.sign_transaction(trxns_eth)
        result = w3.eth.sendRawTransaction(sign_trxns_eth.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        trxns_btctest= create_tx(coin,account,recipient,amount)
        sign_trxns_btctest = account.sign_transaction(trxns_btctest)
        from bit.network import NetworkAPI
        NetworkAPI.broadcast_tx_testnet(sign_trxns_btctest)       
        return tx_hex
    