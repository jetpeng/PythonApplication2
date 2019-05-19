import xmlrpc.client
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('config.json') as config_file:
    data = json.load(config_file)
user_port = data['user_port']

#def submit_sleep():
#   server = xmlrpc.client.ServerProxy("http://127.0.0.1:4000/", allow_none=True)
#   return server.sleep()

#with ThreadPoolExecutor() as executor:
#    sleeps = {executor.submit(submit_sleep) for _ in range(4)}
#    for future in as_completed(sleeps):
#        sleep_time = future.result()
#        print(sleep_time)
ip="http://127.0.0.1:" + str(user_port) + "/"
server = xmlrpc.client.ServerProxy(ip, allow_none=True)
c=input("Select action:\n1:Mine\n2:GetBlock\n3:getBlockCount\n4:getBlockHash\n5.getBlockHeader\nInput'exit'")

while c != "exit":
  if c == "1":      
      print("------------------------")
      a=server.mine()
      a0=str(a).split(',',7)[0]
      a1=str(a).split(',',7)[1]
      a2=str(a).split(',',7)[2]
      a3=str(a).split(',',7)[3]
      a4=str(a).split(',',7)[4]
      a5=str(a).split(',',7)[5]
      a6=str(a).split(',',7)[6]      
      print(a0 + "\n"+ a1 + "\n" + a2+ "\n" + a3+ "\n"  + a5+ "\n" + a6)      
      #print(server.mine())            
      print("------------------------")
  elif c == "2":
      print("------------------------")
      print("Get Block!")
      print(server.full_chain())      
      print("------------------------")
  elif c == "3":
      print("------------------------")
      print("getBlockCount!")      
      print("BlockCount:" + str(server.getBlockcount()))      
      print("------------------------")
      #print("\nRegister_nodes!")
      #print(server.register_nodes("http://127.0.0.1:4000"))      
  elif c == "4":
      print("------------------------")
      print("\ngetBlockHash!")
      c4=input("Input Block Number:")
      print(server.getBlockhash(int(c4)))      
      #print(server.consensus())     
      print("------------------------")
  elif c == "5":
      print("------------------------")
      print("\ngetBlock Header!")
      c5=input("Input Block Header Hash value:")
      print(server.getBlockheaderhash(c5))       
      print("------------------------")
  else:
      print("Input Error, please try it again!")
  c=input("Select action:\n1:Mine\n2:GetBlock\n3:getBlockCount\n4:getBlockHash\n5.getBlockHeader\nInput'exit'")