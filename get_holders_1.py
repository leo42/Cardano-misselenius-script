import requests
import json
################################   EDIT THIS VALUES ##################################################

blockfrost_headers = {"project_id": ""}

policy = "9997c9e9e6d0c2f516a2f2229fa39bff9c30b729e3e02679a422d6ec"
########################################################################

holders = {}

page = 1

while True:
    x = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/"+ policy + "?page=" + str(page) , headers = blockfrost_headers)
    tokens = json.loads(x.text)
    print(tokens)
    if tokens == []:
        break
    for token in tokens:
        if token["quantity"]!= '0':
            x = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/assets/"+ token["asset"] + "/addresses" , headers = blockfrost_headers)
            print(x.text)
            owner = json.loads(x.text)[0]
            
            if owner["address"] in holders:
                holders[owner["address"]]+=1
            else:
                holders[owner["address"]]=1   
    page+=1



with open('Holeders.json', 'w') as outfile:
    json.dump(holders, outfile)    
