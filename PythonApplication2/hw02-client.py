import xmlrpc.client
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('config.json') as config_file:
    data = json.load(config_file)
p2p_port = data['p2p_port']


def submit_sleep():
   server = xmlrpc.client.ServerProxy("http://127.0.0.1:4000/", allow_none=True)
   return server.sleep()

with ThreadPoolExecutor() as executor:
    sleeps = {executor.submit(submit_sleep) for _ in range(4)}
    for future in as_completed(sleeps):
        sleep_time = future.result()
        print(sleep_time)

#server = xmlrpc.client.ServerProxy("http://127.0.0.1:4000/", allow_none=True)
#server = xmlrpc.client.ServerProxy("http://127.0.0.1:4000")
c=input("請選擇動作\n1:Mine()\n2:Full_chain()\n3:Register_nodes()\n4:Consensus()\n離開請輸入'exit'\n")
while c != "exit":
  if c == "1":
      print("\nMine finish!")
      print(server.mine())      
  elif c == "2":
      print("\nList chain!")
      print(server.full_chain())      
  elif c == "3":
      print("\nRegister_nodes!")
      print(server.register_nodes("http://127.0.0.1:4000"))      
  elif c == "4":
      print("\nConsensus!")
      print(server.consensus())     
  else:
      print("Input Error , please try again!")
  c=input("請選擇動作\n1:Mine()\n2:Full_chain()\n3:Register_nodes()\n4:Consensus()\n離開請輸入'exit'\n")