import json
import os
import time
import requests



GRAPHQL_port= ""
headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive', 'DNT': '1'}




dirname = os.path.dirname(__file__)
Batch_size=10

with open(os.path.join(dirname,'delegetors60.json') ) as f:
    stake_address = json.load(f)
payment_address=[]

for stake_addres in stake_address:

    utxo_query = {"query":'{ delegations ( where: {address: { _eq : "' + stake_addres +'" }} )  { address transaction { inputs {address} }} }'}
    r = requests.post(GRAPHQL_port, data=json.dumps(utxo_query), headers=headers)
    data= json.loads( r.text)
    print(data)
    payment_addres = data["data"]["delegations"][0]["transaction"]["inputs"][0]["address"]
    print(payment_addres)
    payment_address.append(payment_addres)



with open(os.path.join(dirname,'delegetors60Payment.json'), 'w') as f:
    json.dump(payment_address, f)



with open(os.path.join(dirname,'delegetors36.json') ) as f:
    stake_address = json.load(f)
payment_address=[]

for stake_addres in stake_address:

    utxo_query = {"query":'{ delegations ( where: {address: { _eq : "' + stake_addres +'" }} )  { address transaction { inputs {address} }} }'}
    r = requests.post(GRAPHQL_port, data=json.dumps(utxo_query), headers=headers)
    data= json.loads( r.text)
    print(data)
    payment_addres = data["data"]["delegations"][0]["transaction"]["inputs"][0]["address"]
    print(payment_addres)
    payment_address.append(payment_addres)



with open(os.path.join(dirname,'delegetors36Payment.json'), 'w') as f:
    json.dump(payment_address, f)