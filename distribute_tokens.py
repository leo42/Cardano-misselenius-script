
from cwAPI import cwAPI
import json
import os
import time

dirname = os.path.dirname(__file__)
Batch_size=10

with open(os.path.join(dirname,'delegetors60Payment.json') ) as f:
    delegetes = json.load(f)

print(len(delegetes))
exit
api = cwAPI()

api.cert=(r'client.crt',r"client.key")
api.ca=r'ca.crt'
api.port="https://localhost:62875"
passphrase= ""


NAME_PREFEX_BRO="BrotherInArmsY2n"
NAME_PREFEX_JEE="Knightzee"
payments=[]
Wallet_id="e2cd4676041d86c216c45c58056eb0aa5c4f78f6"

def wait_for_confirmation(tx_id):
    status = api.Transactions.get(api,Wallet_id,tx_id)["status"]
    while status !="in_ledger":
        print(tx_id+ ": " + status)
        time.sleep(10)
        status = api.Transactions.get(api,Wallet_id,tx_id)["status"]

for i in range(20,len(delegetes)):
    payments.append({
        "address": delegetes[i],
        "amount": {
        "quantity": 2110000,
        "unit": "lovelace"
        },
        "assets": [
        {
            "policy_id": "acac438ec0dc03086df7439f50002d03a3c3fc20bfd74c0e2668094e",
            "asset_name": (NAME_PREFEX_BRO+str(i+1)).encode('utf-8').hex(),
            "quantity": 1
            },
            {
            "policy_id": "acac438ec0dc03086df7439f50002d03a3c3fc20bfd74c0e2668094e",
            "asset_name": (NAME_PREFEX_JEE+str(i+1)).encode('utf-8').hex(),
            "quantity": 1
            }, 
            {
            "policy_id": "a0028f350aaabe0545fdcb56b039bfb08e4bb4d8c4d7c3c7d481c235",
            "asset_name": "484f534b59", #Hosky  #TODO
            "quantity": 3000000
            },
            {
            "policy_id": "2aa9c1557fcf8e7caa049fa0911a8724a1cdaf8037fe0b431c6ac664",
            "asset_name": "50494759546f6b656e", #PIGI
            "quantity": 10000 
            },
            {
            "policy_id": "c53f04773bc33549a2ea5ee4970c6819af3d81871243f6b2bb28e04b",
            "asset_name": "444f4745414441", #DOGEADA
            "quantity": 2000
            }

        ]
    })

    if len(payments) >= Batch_size:
        tx = api.Transactions.create(api,walletId=Wallet_id,passphrase=passphrase,payments=payments)
        print(tx)
        tx_id=tx["id"]
        wait_for_confirmation(tx_id)
        print(tx)
        payments=[]

tx = api.Transactions.create(api,walletId=Wallet_id,passphrase=passphrase,payments=payments)
tx_id=tx["id"]
wait_for_confirmation(tx_id)
print(tx)
print(tx)   
    
