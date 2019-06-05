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
import ecdsa

class Blockchain:
  def __init__(self):
   with open('config.json') as config_file:
    data = json.load(config_file)
   thenodebeneficiary = data['beneficiary']
   self.chain = []
   self.current_transactions = []
   self.new_block(nonce='00000001',prev_block='00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000', version='00000002', 
                  transactions_hash='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', thenodetarget='0000100000000000000000000000000000000000000000000000000000000000', beneficiary = thenodebeneficiary)
    
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
            if block['prev_block'] != last_block_hash:
                return False
            # pow是否正確?
            if not self.valid_proof(last_block['nonce'], block['nonce'], last_block_hash):
                return False
            last_block = block
            current_index += 1
        return True

  def resolve_conflicts(self):      
        #最長鏈原則
        #neighbours = self.nodes
        new_chain = None
        #找出最長鏈
        max_length = len(self.chain)
        print(max_length)
        #Grab and verify the chains from all the nodes
  #      for node in neighbours:
            #response = requests.get(f'http://{node}/chain')            
            #if response.status_code == 200:
            #    length = response.json()['length']
            #    chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
            #    if length > max_length and self.valid_chain(chain):
            #        max_length = length
            #        new_chain = chain
        # 看哪個是最長鏈
  #       if new_chain:
  #          self.chain = new_chain
  #          return True
  #      return False
  def new_block(self, nonce, prev_block,version, transactions_hash, thenodetarget, beneficiary):    
        #建block
        print(self.current_transactions)        
        print(len(self.chain))
        print(self.chain)
        #print(self.chain['transactions'])     
        #print(self.chain[0]['transactions']['signature'])
        trans_hash='123'
        #print(self.current_transactions[0][])
        #if (self.current_transactions == '[]'):
        # trans_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        #else :
        #     i=0
        #     allsignature=''
        #     while i<len(self.current_transactions):
        #      benevalue=self.current_transactions[i]
        #      benevalue2=benevalue['signature']                 
        #      print(benevalue)
        #      allsignature = allsignature + benevalue2
        #      i=i+1     
        #     trans_hash = hashlib.sha256(allsignature).hexdigest()
             
        #print(trans_hash)       

        block = {
            'version' : "00000002",
            'index': len(self.chain) + 1, 
            'transactions': self.current_transactions,
            'transactions_hash' : trans_hash,
            'target': thenodetarget,
            'nonce': nonce,
            'beneficiary' : beneficiary,
            'prev_block': prev_block or self.hash(self.chain[-1]),
        }

        # 加到鏈後
        self.current_transactions = []
        self.chain.append(block)
        return block

  def new_transaction(self,trans_nonce,sender_pub_key,value,signature,fee,to):
        self.current_transactions.append({
            'nonce': trans_nonce,
            'sender_pub_key': sender_pub_key,
            'value': value,
            'signature' : signature,
            'fee' : fee,
            'to' : to,
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
        transactions_hash=last_block['transactions_hash']
        target=last_block['target']
        #last_proof = last_block['nonce']
        last_proof = last_block['prev_block']
        last_hash = self.hash(last_block)        
        print(last_hash) 
        nonce = 0        
        #while self.valid_proof(last_proof, nonce, last_hash, version, transactions_hash, target) is False:
        vr = self.valid_proof( nonce, last_hash, version, transactions_hash, target)
        while vr >= target:
            nonce += 1     
            vr=self.valid_proof( nonce, last_hash, version, transactions_hash, target)                        
            print(vr)
        return nonce,vr

  @staticmethod
  def valid_proof(nonce, last_hash, version, transactions_hash, target):
        #找出pow
        #guess = f'{version}{last_proof}{transactions_hash}{nonce}{last_hash}'.encode()
        guess = f'{version}{last_hash}{transactions_hash}{target}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()        
        return guess_hash


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

#mine
def mine():
    last_block = blockchain.last_block        
    nonce,prev_block = blockchain.proof_of_work(last_block)

    # The sender is "0" to signify that this node has mined a new coin.
  #  blockchain.new_transaction(   
  #   trans_nonce = '123',
  #   sender_pub_key = public_key,
  #   value = 0,
  #   signature = '8199dcbb298a8085325892d956b85e7f1566006cb9dc2b2e36f514f9b9d45be28c3c4dc46eae77e0a18a3a8fcccc313e8b8349d5057eb370ca7c0eccea407237',
  #   fee = thenodefee,
  #   to='4643bb6b393ac20a6175c713175734a72517c63d6f73a3ca90a15356f2e967da03d16431441c61ac69aeabb7937d333829d9da50431ff6af38536aa262497b27',
  #  )

    # Forge the new Block by adding it to the chain
    #這行有錯
    #prev_block = blockchain.hash(last_block)    

    version="00000002"
    transactions_hash="0000000000000000000000000000000000000000000000000000000000000000"
    target = thenodetarget
    beneficiary = thenodebeneficiary
    block = blockchain.new_block(nonce, prev_block, version, transactions_hash, target,beneficiary)      

    ip="http://127.0.0.1:" + str(node2p2p_port) + "/"
    print(ip)
    blockchain.resolve_conflicts()    
    try:
     server3 = xmlrpc.client.ServerProxy(ip, allow_none=True)
     server3.sendblock(target,block['version'],str(block['index']),block['transactions_hash'],str(block['transactions']),str(block['nonce']),block['prev_block'],block['beneficiary'])
    except:
     print("no neighbor node!")     
    
    #ip="http://127.0.0.1:" + str(node3p2p_port) + "/"
    #server4 = xmlrpc.client.ServerProxy(ip, allow_none=True)
    #server4.sendblock()

    #存到json but HW3改成不用存json
    #file_name = 'blockinfo.json'    
    #data = {
    #    "version": block['version'], 
    #    "index": str(block['index']), 
    #    "transactions_hash": block['transactions_hash'],
    #    "beneficiary": block['thenodebeneficiary'],
    #    "transactions": str(block['transactions']), 
    #    "nonce": str(block['nonce']), 
    #    "prev_block": block['prev_block'],
    #    "beneficiary": block['beneficiary']
    #}       
    
    #with open(file_name,'a') as file_object:
    # json.dump(data,file_object)    
    return "message: New Block Forged" , "version:" + block['version'] , "index:" + str(block['index']) , "transactions_hash:" + block['transactions_hash'] , \
        "transactions:" + str(block['transactions']) , "nonce:" + str(block['nonce']) , \
        "prev_block:" + block['prev_block'], "beneficiary:" + str(block['beneficiary'])

def sendblock(target,version,index,transactions_hash,transactions,nonce,prev_block,beneficiary):
    #block = blockchain.new_block(nonce, prev_block, version, transactions_hash, target,beneficiary)      
    print("received block:\n")
    print(self.chain[-1])

def signkeys(nonce,public,to,value,fee): #[RW: Add for key signing]
    
    block2sign = str(nonce) + str(public) + str(to) + str(value) + str(fee)
    block_hash = hashlib.sha256(block2sign.encode('utf8')).hexdigest()
    
    priv = "c0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0de"
    pv = ecdsa.SigningKey.from_string(bytes.fromhex(priv), curve=ecdsa.SECP256k1)
    print ("===================================================")
    block_signed = pv.sign(bytes.fromhex(block_hash))
    print(block_hash)
    print ("===================================================")
    print(block_signed.hex())
    return block_signed.hex()

def verikeys(block_signed_2): #[RW: Add for key verifying]

    pb = ecdsa.VerifyingKey.from_string(bytes.fromhex(public), curve=ecdsa.SECP256k1)
    result = pb.verify(block_signed_2, bytes.fromhex(block_hash))
    return result



 #execute transation,not yet finish
 #app.route('/transactions/new', methods=['POST'])
def new_transaction(nonce,sender_pub_key,value,signature,fee,to): 
        index = blockchain.new_transaction(nonce, sender_pub_key, value, signature, fee, to)
        #return self.last_block['index'] + 1
        return 'message: Transaction will be added to Block'

#def new_transaction():
    #values = request.get_json()
    # Check that the required fields are in the POST'ed data
    #required = ['sender', 'recipient', 'amount']
    #if not all(k in values for k in required):
    #    return 'Missing values', 400
    # 新的交易

    #index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    #response = {'message': f'Transaction will be added to Block {index}'}
    #return response

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

def getbalance(c7):  
     i=0

     balance=0            
     #a1=blockchain.chain[1]
     #a2=a1['transactions']     
     #print(a2[0]['to'])   
     while i<len(blockchain.chain):#-2:
      benevalue=blockchain.chain[i]
      benevalue2=benevalue['beneficiary']
      benevalue3=benevalue['transactions']        
     
      if benevalue2 == c7:
        balance = balance+1000  
        print(balance)
        if str(benevalue3) != "[]":           
         j=0
         while j<len(benevalue3):
          if str(benevalue3[j]['to']) == c7:       
           thevalue=int(benevalue3[j]['value'])
           balance=balance+thevalue
          if benevalue3[j]['sender_pub_key'] == c7:
           thevalue2=int(benevalue3[j]['value'])
           thevalue3=int(benevalue3[j]['fee'])
           balance=balance-thevalue2-thevalue3   
           print(balance)
          j=j+1
      i=i+1     
      print(balance)
     return balance

def sendtoaddress(c6,c62):    
    address = c6
    amount = c62
    signatureresult = signkeys('0x0000000000000000',public_key,address,amount,thenodefee)   
    blockchain.new_transaction(   
     trans_nonce = '0x0000000000000000',
     sender_pub_key = public_key,
     value = amount,
     signature = signatureresult,
     fee = thenodefee,
     to=address,
    )
    return "finish!"

def getBlockheaderhash(c5):    
    i=0;   
    b="abc"         
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

thenodebeneficiary = data['beneficiary']
mining = data['mining']
thenodefee = data['fee']
thenodetarget = data['target']
public_key = data['wallet']['public_key']
private_key = data['wallet']['private_key']

# run server
def run_server():    
    ip="127.0.0.1"
    server_addr = (ip , int(user_port))
    server = SimpleThreadedXMLRPCServer(server_addr)
    server.register_function(sleep, 'sleep')
    server.register_function(mine)
    #server.register_function(resolve_conflicts)
    server.register_function(getBlockcount)
    server.register_function(getBlockhash)
    server.register_function(getBlockheaderhash)
    server.register_function(full_chain)
    server.register_function(register_nodes)
    server.register_function(consensus)
    server.register_function(sendtoaddress)    
    server.register_function(getbalance)    
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
   # c=input('exit')
   # while c != "exit":
   #     print(c)

    #run_server()  
