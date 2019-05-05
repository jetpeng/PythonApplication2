from xmlrpc.server import SimpleXMLRPCServer

def speak_your_words(s):
    print("message from client:", s)
    return "message from server: " + s

server = SimpleXMLRPCServer(("localhost",9999)) # 绑定端口
server.register_function(speak_your_words) # 注册函数
server.serve_forever() #启动监听