import subprocess, os
import requests 
import json 
import time
import sys
from numpy.random import choice
from tinydb import TinyDB, Query

SELF_ADDRESS="addr1v8w6hyql9hw8p3ac4lj97u79953e6ftm5cxn3uwan48svecuedw7f"
output_address="addr1qy0utwwt9ywm8p4t8j0dgd87kardy40vv7de3m32v4e2tuus0jf4y3gl92gq5qlg3euh5t278stdussplkgv9n7kw4vslzga5s"
POLICY_ID="acac438ec0dc03086df7439f50002d03a3c3fc20bfd74c0e2668094e"


Batch_size=10

db_avaialble = TinyDB('db_available.json')
User = Query()
NAME_PREFEX="BrotherInArmsY2n"

my_env = os.environ.copy()
#my_env["PATH"] = "/root/cardano-node:" + my_env["PATH"]
my_env["CARDANO_NODE_SOCKET_PATH"] = "/home/leo/nodes/relay/node.socket"
asset="Testzee01".encode('utf-8').hex()



def mint(knightzees,utxo):
    min_utxo=1819011

    utxos=get_utxos()
    tokens=""
    for knightzee in knightzees:
        asset= (NAME_PREFEX+str(knightzee)).encode('utf-8').hex()
        if tokens=="":
            tokens = "1 "+POLICY_ID+"." + asset
        else:
            tokens = "1 "+POLICY_ID+"." + asset + "+" + tokens
    fee=180989
    tx_out = output_address+"+"+ str(min_utxo) + "+"+ tokens
    

    process = subprocess.check_output(['/home/leo/.local/bin/cardano-cli', "transaction", "calculate-min-required-utxo", 
    "--protocol-params-file", "protocol.json",
    "--tx-out", tx_out    ], env= my_env).decode('utf-8')
    min_utxo=int(process.split()[1])

    change= int(utxos[utxo]) - min_utxo - fee

    tx_out_change = SELF_ADDRESS+"+"+ str(change) 


    process = subprocess.check_output(['/home/leo/.local/bin/cardano-cli', 'transaction', 'build-raw', 
    "--fee", str(fee), 
    "--tx-in", utxo, 
    "--tx-out", tx_out ,
    "--tx-out", tx_out_change ,
    "--mint", tokens, \
    "--mint-script-file", "policy.script", \
    "--invalid-hereafter", "53635271", \
    "--metadata-json-file", "metadata.json", \
    "--out-file", "matx.raw"  ], env= my_env).decode('utf-8')

    process = subprocess.check_output(['/home/leo/.local/bin/cardano-cli', "transaction", "calculate-min-fee", 
    "--tx-body-file", "matx.raw", 
    "--tx-in-count", "1", 
    "--tx-out-count", "2", 
    "--witness-count", "1", 
    "--mainnet", 
    "--protocol-params-file", "protocol.json"], env= my_env).decode('utf-8')
    fee=int(process.split()[0])


    change= int(utxos[utxo]) - min_utxo - fee

    tx_out = output_address+"+"+ str(min_utxo) + "+"+ tokens
    tx_out_change = SELF_ADDRESS+"+"+ str(change) 

    process = subprocess.check_output(['/home/leo/.local/bin/cardano-cli', 'transaction', 'build-raw', 
    "--fee", str(fee), 
    "--tx-in", utxo, 
    "--tx-out", tx_out ,
    "--tx-out", tx_out_change ,
    "--mint", tokens, \
    "--mint-script-file", "policy.script", \
    "--invalid-hereafter", "53635271", \
    "--metadata-json-file", "metadata.json", \
    "--out-file", "matx.raw"  ], env= my_env).decode('utf-8')

    process = subprocess.check_output(["cardano-cli", "transaction", "sign",
            "--signing-key-file", "payment.skey",
            "--mainnet",
            "--tx-body-file", "matx.raw",
            "--out-file", "matx.signed"
    ], env= my_env).decode('utf-8')

    print("Output: " + process)



    process = subprocess.check_output(["cardano-cli", "transaction", "submit", "--tx-file", "matx.signed",  "--mainnet"], env= my_env).decode('utf-8')

    print("Output: " + process)

def get_utxos():
    utxos={}
    process = subprocess.check_output(["cardano-cli", "query", "utxo", "--address", SELF_ADDRESS, "--mainnet" ], env= my_env).decode('utf-8')
    process_lines = process.strip().split("\n")[2:]
    for line in process_lines:
        line_list= line.split()
        print(line_list)
        utxos[line_list[0]+"#"+line_list[1]]=line_list[2]

    return utxos



def wait_for_confirmation(utxo):
    open_utxos=get_utxos()
    while utxo in open_utxos:
        
        print("Wating on :"+utxo)
        time.sleep(10)
        open_utxos=get_utxos()

def extra_meta(knightzee):
    metadata = knightzee
    metadata["name"] = "Brother In Arms Y2 " +   str(knightzee["serial"])
    metadata["mediaType"] = "image/png"
    metadata["Description"] =  "A badge of Honor for the loyal Brothers of BSP during 2021."
    metadata["Recipients"] = "Anyone delegated to BSP for over 60 Epochs during 2021."
    metadata["Note"] = "You are the strength behind the shield!"
    metadata["files"]=[{"mediaType": "image/png", "name": NAME_PREFEX + str(knightzee["serial"]), "src": knightzee["image"] }]
    return metadata

def generate_metadata(knigtzeez_list):
    knigtzeez_meta = {}
    knigtzeez_serials = []
    for knigtzeez in knigtzeez_list:
        name=NAME_PREFEX + str(knigtzeez["serial"])
        knigtzeez_meta[name] = extra_meta(knigtzeez)
        knigtzeez_serials.append(str(knigtzeez["serial"]))
    print(knigtzeez_meta)    
    metadata= {"721" : { POLICY_ID:  knigtzeez_meta  }}

    print(metadata)

    with open("metadata.json","w") as metadata_file: 
        json.dump(metadata,metadata_file)

    return knigtzeez_serials


def send_batch( knigtzeez_list):
    serials = generate_metadata(knigtzeez_list)
    open_utxos = get_utxos()
    utxo=list(open_utxos.keys())[0]
    mint(serials,utxo)
    wait_for_confirmation(utxo)
    knigtzeez_list=[]
    return knigtzeez_list

if __name__ == "__main__":
        
    knigtzeez_list=[]
    for i in range(1,100):
        knigtzeez_list.append({"serial":i,"image":"ipfs://QmQfMrpwTghviZD4sfkKQZ4UMkKD8bgetRpK1H9ww3gBZh"})
        if  len(knigtzeez_list)>=Batch_size:
            knigtzeez_list = send_batch(knigtzeez_list)


    knigtzeez_list = send_batch(knigtzeez_list)



        

