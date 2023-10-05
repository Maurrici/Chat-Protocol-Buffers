import protobufjs from "protobufjs"
import net from "net"
import readline from "readline-sync"

// Protocol Buffer methods
const root = await protobufjs.load("chat.proto")
var ChatRequest = root.lookupType("ChatRequest")
var ChatMessage = root.lookupType("ChatMessage") 

function createMessage(action, value) {
    let request = {
        action,
        value
    }

    var errMsg = ChatRequest.verify(request);
    if (errMsg) throw Error(errMsg);

    var message = ChatRequest.create(request);
    console.log(message);
    return message
}

function getObjectFromData(data) {
    let message = ChatMessage.decode(data);
    let object = ChatMessage.toObject(message);
    
    return object
}

// User input
var userName = readline.question("Nickname:");
const host = "127.0.0.1";
const port = 7000;

// Socket
const client = net.createConnection(port, host, () => {
    console.log("Connected");
    let message = createMessage("/ENTRAR", userName)
    var buffer = ChatRequest.encode(message).finish()
    client.write(buffer);
})

client.on("data", (data) => {
    let message = getObjectFromData(data);
    console.log(`Received: ${data}`);
    console.log(message);
})

client.on("error", (error) => {
    console.log(`Error: ${error.message}`);
})

client.on("close", () => {
    console.log("Connection closed");
})

