from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from socketserver import ThreadingMixIn
import threading
import hashlib
import time                                                                   
import random  
import json
from io import StringIO
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests

class Blockchain:
  def __init__(self):
   self.chain = []
   self.nodes = set()
   self.current_transactions = []
   self.new_block(nonce='00000001',previous_hash='00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000', version='00000001', merkle_root='0000000000000000000000000000000000000000000000000000000000000000', target='0001000000000000000000000000000000000000000000000000000000000000')

   
  def register_node(self, address):
        #申請註冊，加入新node        
        print("call blockchain.register_node")  
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:            
            self.nodes.add(parsed_url.path)
        else:
            return "Invalid URL"   

  def valid_chain(self, chain):
        #check blockchain is valid?
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # check hash value
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False
            # pow是否正確?
            if not self.valid_proof(last_block['nonce'], block['nonce'], last_block_hash):
                return False
            last_block = block
            current_index += 1
        return True

  def resolve_conflicts(self):
        #最長鏈原則
        neighbours = self.nodes
        new_chain = None
        #找出最長鏈
        max_length = len(self.chain)

        #Grab and verify the chains from all the nodes
        for node in neighbours:
            #response = requests.get(f'http://{node}/chain')            
            #if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # 看哪個是最長鏈
        if new_chain:
            self.chain = new_chain
            return True
        return False

  def new_block(self, nonce, previous_hash,version, merkle_root, target):    
        #建block
        block = {
            'version' : "00000001",
            'index': len(self.chain) + 1,
            #'timestamp': time(), 
            'transactions': self.current_transactions,
            'merkle_root' : "0000000000000000000000000000000000000000000000000000000000000000",         
            "target": "0001000000000000000000000000000000000000000000000000000000000000",
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 加到鏈後
        self.current_transactions = []
        self.chain.append(block)
        return block

  def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

  @property
  def last_block(self):
     return self.chain[-1]

  @staticmethod
  def hash(block):
        #使用一次sha256     
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

  def proof_of_work(self, last_block):
        #找出pow
        version=last_block['version']
        merkle_root=last_block['merkle_root']
        target=last_block['target']
        last_proof = last_block['nonce']
        last_hash = self.hash(last_block)        
        print(last_hash) 
        nonce = 0        
        #while self.valid_proof(last_proof, nonce, last_hash, version, merkle_root, target) is False:
        vr = self.valid_proof( nonce, last_hash, version, merkle_root, target)
        while vr >= target:
            nonce += 1     
            vr=self.valid_proof( nonce, last_hash, version, merkle_root, target)                        
            print(vr)
        return nonce,vr

  @staticmethod
  def valid_proof(nonce, last_hash, version, merkle_root, target):
        #找出pow
        #guess = f'{version}{last_proof}{merkle_root}{nonce}{last_hash}'.encode()
        guess = f'{version}{last_hash}{merkle_root}{target}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()        
        return guess_hash


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

#mine
def mine():
    last_block = blockchain.last_block        
    nonce,previous_hash = blockchain.proof_of_work(last_block)

    # The sender is "0" to signify that this node has mined a new coin.
    #blockchain.new_transaction(
    #    sender="0",
    #    recipient=node_identifier,
    #    amount=1,
    #)

    # Forge the new Block by adding it to the chain
    #這行有錯
    #previous_hash = blockchain.hash(last_block)    

    version="00000001"
    merkle_root="0000000000000000000000000000000000000000000000000000000000000000"
    target="0000100000000000000000000000000000000000000000000000000000000000"
    block = blockchain.new_block(nonce, previous_hash, version, merkle_root, target)      
    ip="http://127.0.0.1:" + str(node2p2p_port) + "/"
    print(ip)
    try:
     server3 = xmlrpc.client.ServerProxy(ip, allow_none=True)
     server3.sendblock(target,block['version'],str(block['index']),block['merkle_root'],str(block['transactions']),str(block['nonce']),block['previous_hash'])
    except:
     print("connection error!")     
    
    #ip="http://127.0.0.1:" + str(node3p2p_port) + "/"
    #server4 = xmlrpc.client.ServerProxy(ip, allow_none=True)
    #server4.sendblock()

    #存到json
    file_name = 'blockinfo.json'    
    data = {
        "version": block['version'], 
        "index": str(block['index']), 
        "merkle_root": block['merkle_root'],
        "transactions": str(block['transactions']), 
        "nonce": str(block['nonce']), 
        "previous_hash": block['previous_hash']
    }       
    
    with open(file_name,'a') as file_object:
     json.dump(data,file_object)     

    return "message: New Block Forged" , "version:" + block['version'] , "index:" + str(block['index']) , "merkle_root:" + block['merkle_root'] , \
        "transactions:" + str(block['transactions']) , "nonce:" + str(block['nonce']) , \
        "previous_hash:" + block['previous_hash']

def sendblock(target,version,index,merkle_root,transactions,nonce,previous_hash):
    block = blockchain.new_block(nonce, previous_hash, version, merkle_root, target)      

 #execute transation,not yet finish
 #app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # 新的交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return response

#找出chain
def full_chain():
    return 'chain:' , blockchain.chain

#回傳Block數量
def getBlockcount():    
    return len(blockchain.chain)

def getBlockhash(c4):    
    if c4<len(blockchain.chain):
     return blockchain.chain[c4]
    else:
     return "out of data!"

def getBlockheaderhash(c5):    
    i=0;   
    b="abc"
    #findout=str(blockchain.chain[0])
    #b=findout.find(c5)
    #return b           
    while i<len(blockchain.chain):
      findvalue=str(blockchain.chain[i])
      findout=findvalue.find(c5)
      if findout != -1:
           b=blockchain.chain[i]
      i=i+1

    if b != "abc":
     return b
    else:
     return "Can't find it!"

    #while (c5 != (blockchain.chain[c2].hash))：
    # i++
    #return "out of data!"

#register node
def register_nodes(nodes):     
    if nodes is None:
        return "Error: Please supply a valid list of nodes"
    for node in nodes:
        blockchain.register_node(nodes)
    return "message:New nodes have been added,total_nodes:" , list(blockchain.nodes)      

#consensus
#@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
            return ('new_chain' + blockchain.chain)        
    else:
            return ('chain' + blockchain.chain)             

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass
# sleep for random number of seconds
def sleep():
    r = random.randint(2, 10)
    print('sleeping {} seconds'.format(r))
    time.sleep(r)
    return 'slept {} seconds, exiting'.format(r)

with open('config.json') as config_file:
    data = json.load(config_file)
p2p_port = data['p2p_port']
user_port = data['user_port']
node2p2p_port = data['neighbor_list'][0]['p2p_port']
node2user_port = data['neighbor_list'][0]['user_port']
node3p2p_port = data['neighbor_list'][1]['p2p_port']
node3user_port = data['neighbor_list'][1]['user_port']

# run server
def run_server():    
    ip="127.0.0.1"
    server_addr = (ip , int(user_port))
    server = SimpleThreadedXMLRPCServer(server_addr)
    server.register_function(sleep, 'sleep')
    server.register_function(mine)
    server.register_function(getBlockcount)
    server.register_function(getBlockhash)
    server.register_function(getBlockheaderhash)
    server.register_function(full_chain)
    server.register_function(register_nodes)
    server.register_function(consensus)
    print('listening on {} user port {}'.format(ip, user_port))    
    server.serve_forever()

def run_server2():    
    ip="127.0.0.1"
    server_addr2 = (ip , int(p2p_port))
    server2 = SimpleThreadedXMLRPCServer(server_addr2)
    server2.register_function(sendblock)    
    print('listening on {} p2p port {}'.format(ip, p2p_port))
    server2.serve_forever()

def main():
    added_thread = threading.Thread(target=run_server)
    added_thread2 = threading.Thread(target=run_server2)
    added_thread.start()
    added_thread2.start()
    #print(threading.active_count()) # 2
    #print(threading.enumerate()) # [<_MainThread(MainThread, started 140736627270592)>, <Thread(Thread-1, started 123145466363904)>]
    #print(threading.current_thread()) #<_MainThread(MainThread, started 140736627270592)>


if __name__ == '__main__':
    main()
    c=input('exit')
    while c != "exit":
        print(c)

    #run_server()  
