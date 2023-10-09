import chat_pb2 as ChatProto
import socket 
import time
import threading

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
    message.ParseFromString(data)

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

users = {}
connections = []

def handle_client(con, cliente):
    while True:
        print("Waiting 2...")
        buffer = con.recv(1024) 
        print(buffer)

        request = getObjectFromData(buffer)
        print(request)

        if request.action == "/ENTRAR":
            if len(users) < 4:
                users[cliente] = request.value
                buffer = createMessage("/ENTRAR", request.value, f"{request.value} entrou no chat!")
                for conn in connections:
                    conn.send(buffer)
            else:
                buffer = createMessage("/FECHADO", request.value, "Desculpe, a sala esta cheia no momento, tente novamente em alguns minutos")
                con.send(buffer)
                
        elif request.action == "/MENSAGEM":
            buffer = createMessage("/MENSAGEM", users[cliente], request.value)
            for conn in connections:
                conn.send(buffer)
            
        elif request.action == "/USUARIOS":
            buffer = createMessage("/USUARIOS", "", ", ".join(users.values()))
            con.send(buffer)
            
        elif request.action == "/NICK":
            old_name = users[cliente]
            new_name = request.value
            users[cliente] = new_name
            buffer = createMessage("/NICK", new_name, f"{old_name} agora se chama {new_name}")
            for conn in connections:
                conn.send(buffer)
            
        elif request.action == "/SAIR":
            user_name = users.pop(cliente)
            connections.remove(con)
            con.close()
            buffer = createMessage("/SAIR", user_name, f"{user_name} saiu do chat!")
            for conn in connections:
                conn.send(buffer)

while True:
    con, cliente = serv_socket.accept() 
    connections.append(con)
    thread = threading.Thread(target=handle_client, args=(con, cliente))
    thread.start()

serv_socket.close()