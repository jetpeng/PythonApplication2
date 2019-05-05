import xmlrpc.client
 
server = xmlrpc.client.ServerProxy("http://localhost:9999")
print(server.speak_your_words("a"))
#print(server.pow(2, 9))
#print(server.add("abc", "32321"))
#server.add(24, 11)