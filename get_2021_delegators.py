import requests
import json
import os
dirname = os.path.dirname(__file__)

GRAPHQL_port1= ""
GRAPHQL_port2= ""
headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive', 'DNT': '1'}
GRAPHQL_port= GRAPHQL_port1
def port_swap():
    global GRAPHQL_port
    if GRAPHQL_port == GRAPHQL_port1:
        GRAPHQL_port = GRAPHQL_port2
    else:
        GRAPHQL_port = GRAPHQL_port1   
#data = {"query":'{activeStake (where: { stakePoolHash: { _eq : "89eba2781e5cd11ccda6be56503702a39e9941e522f04cd5bba22957" } _and: {epochNo: { _eq: 300 }} }) { address amount  epochNo   } }'}
#r = requests.post(GRAPHQL_port, data=json.dumps(data), headers=headers)
#print (r.text)
#json_data = json.loads( r.text)
delegates={}
counter=0
for epoch in range(239,312):
    print(epoch)
    try:
        data = {"query":'{activeStake (where: { stakePoolHash: { _eq : "89eba2781e5cd11ccda6be56503702a39e9941e522f04cd5bba22957" } _and: {epochNo: { _eq: ' + str(epoch) + ' }} }) { address amount  epochNo   } }'}
        r = requests.post(GRAPHQL_port, data=json.dumps(data), headers=headers)
        json_data = json.loads( r.text)
        stakes= json_data["data"]["activeStake"]
    except:
        stakes = []
    if stakes == []:
        print("retry: "+ str(epoch) )
        port_swap()
        try:
            r = requests.post(GRAPHQL_port, data=json.dumps(data), headers=headers)
            json_data = json.loads( r.text)
            stakes= json_data["data"]["activeStake"]
        except:
            continue
        
    counter=0
    for stake in stakes:
        counter+=1
        if int(stake["amount"]) > 50000000 :
            if stake["address"] not in delegates:
                delegates[stake["address"]] = { "epochs": 1 , "amount": int(stake["amount"])}
            else:
                delegates[stake["address"]]["epochs"] += 1  
                delegates[stake["address"]]["amount"] += int(stake["amount"])
    print("counter: " + str(counter))
print(delegates)    

with open(os.path.join(dirname,'delegetors.json'), 'w') as f:
    json.dump(delegates, f)

# next_hash = json_data['data']['cardano']['tip']['hash']

# current_epoch = json_data['data']['cardano']['tip']["epochNo"]
# print (next_hash)
# data = {str(current_epoch): { "fees" : 0 , "transactions" : 0 , "totalOutput": 0 }, str(current_epoch-1): { "fees" : 0 , "transactions" : 0 , "totalOutput": 0 } ,str(current_epoch-2) : { "fees" : 0 , "transactions" : 0 , "totalOutput": 0 } }
# print(data)

# while True:
#     request = {"query":'{ blocks (where: {  hash: {  _eq: "' + next_hash + '"}} ){epochNo,fees,forgedAt , number, previousBlock {hash}, transactions_aggregate{aggregate {count sum {totalOutput}} } }}'}
#     r = requests.post(GRAPHQL_port, data=json.dumps(request), headers=headers)
#     print (r.text)
#     json_data =   json.loads( r.text)
#     next_hash = json_data['data']['blocks'][0]["previousBlock"]['hash']
#     epoch =  json_data['data']['blocks'][0]["epochNo"]
#     if epoch < (current_epoch - 2):
#         break
#     data[str(epoch)]["fees"] += json_data['data']['blocks'][0]["fees"]
#     data[str(epoch)]["transactions"] += int(json_data['data']['blocks'][0]["transactions_aggregate"]["aggregate"]["count"])
#     if json_data['data']['blocks'][0]["transactions_aggregate"]["aggregate"]["sum"]["totalOutput"] != None:
#         data[str(epoch)]["totalOutput"] += int(json_data['data']['blocks'][0]["transactions_aggregate"]["aggregate"]["sum"]["totalOutput"])
#     print(data)
