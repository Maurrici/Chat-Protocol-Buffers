import chat_pb2 as ChatProto
import socket 
import time

# Protocol buffers methods
def createMessage(type, userName, message):
    messageData = ChatProto.ChatMessage()
    messageData.type = type
    messageData.userName = userName
    messageData.message = message
    buffer = messageData.SerializeToString()

    return buffer

def getObjectFromData(data):
    message = ChatProto.ChatRequest()
    message.ParseFromString(buffer)

    return message

# Socket config
host = '' 
port = 7000 
addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr) 
serv_socket.listen(10) 

print("Waiting...")
con, cliente = serv_socket.accept() 
while True:
    print("Waiting 2...")
    buffer = con.recv(1024) 
    print(buffer)

    message = getObjectFromData(buffer)
    print(message)

    buffer = createMessage("/MENSAGEM", "Server", message.value)
    con.send(buffer)
    time.sleep(0.5)
    buffer = createMessage("/ENTRAR", "Irineu", "")
    con.send(buffer)
    time.sleep(0.5)
    buffer = createMessage("/NICK", "", "Irineu agora se chama: Irineu vc não sabe nem eu")
    con.send(buffer)
    # buffer = createMessage("/USUARIOS", "", "1 - Irineu\n 2 - Joaquin\n")
    # con.send(buffer)
    time.sleep(0.5)
    buffer = createMessage("/SAIR", "", "Irineu saiu do chat!")
    con.send(buffer)
        
serv_socket.close()