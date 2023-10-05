import chat_pb2 as ChatProto
import socket 

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

while True:
    print("Waiting...")
    con, cliente = serv_socket.accept() 
    buffer = con.recv(1024) 
    print(buffer)

    message = getObjectFromData(buffer)
    print(message)

    buffer = createMessage("WELCOME", message.value, "Seja bem vindo!")
    con.send(buffer)

serv_socket.close()