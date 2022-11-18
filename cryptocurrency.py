from eth_account import Account
from bitcoin import *
import secrets

def getBTC():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    #print("SAVE BUT DO NOT SHARE THIS:", private_key)
    public_key = privtopub(private_key)
    accBTC = pubtoaddr(public_key)
    #print("BTC Address: ", accBTC)
    return accBTC

def getETH():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    #print ("SAVE BUT DO NOT SHARE THIS:", private_key)
    accETH = Account.from_key(private_key)
    #print("ETH Address:", accETH.address)
    return accETH.address