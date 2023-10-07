import protobufjs from "protobufjs"
import net from "net"
import readline from "readline-sync"
import blessed from "neo-blessed"

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
    return ChatRequest.encode(message).finish()
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
    let buffer = createMessage("/MENSAGEM", userName)
    client.write(buffer);

    client.on("data", (data) => {
        let message = getObjectFromData(data);
        handleMessage(message)
    })
    
    client.on("error", (error) => {
        messageList.addItem("--------- Um erro inesperado aconteceu ---------");
    })
    
    client.on("close", () => {
        messageList.addItem("--------- Você saiu do chat! ---------");
    })
    
    // Business Logic
    const SPECIAL_ACTIONS = ["/USUARIOS", "/NICK", "/SAIR"]
    
    function handleMessage(message) {
        let text;
        switch (message.type) {
            case "/ENTRAR":
                text = `--------- ${message.userName} entrou no Chat! ---------`
                messageList.addItem(text);
                break
            case "/MENSAGEM":
                messageList.addItem(`${message.userName}: ${message.message}`)
                break
            case "/USUARIOS":
                text = `--------- Lista de usuários: ${message.message} ---------`
                messageList.addItem(text);
                break
            case "/NICK":
                text = `--------- ${message.message} ---------`
                messageList.addItem(text);
                break
            case "/SAIR":
                text = `--------- ${message.message} ---------`
                messageList.addItem(text);
                break
        }  
        messageList.scroll(100)
        screen.render() 
    }
    
    function sendMessage(text) {
        let specialAction = SPECIAL_ACTIONS.find(action => text.includes(action))
    
        if(specialAction) {
            let action = specialAction
            let value = ""
    
            if(specialAction === "/NICK") {
                value = text.replaceAll(specialAction).trim()
            }
    
            let buffer = createMessage(action, value)
            client.write(buffer)
        } else {
            let buffer = createMessage("/MENSAGEM", text)
            client.write(buffer)
        }
    }
    
    // Chat UI
    const screen = blessed.screen({ smartCSR: true, title: "Chat - Protocol Buffers"})
    
    var messageList = blessed.list({
        align: 'left',
        mouse: true,
        keys: true,
        width: '100%',
        height: '90%',
        top: 0,
        left: 0,
        scrollable: true,
        scrollbar: {
          ch: ' ',
          inverse: true,
        },
        items: [],
    });
    
    var inputField = blessed.textarea({
        bottom: 0,
        height: '10%',
        inputOnFocus: true,
        padding: {
          top: 1,
          left: 2,
        },
        style: {
          fg: '#000000',
          bg: '#FFFFFF',
    
          focus: {
            fg: '#000000',
            bg: '#FFFFFF',
          },
        },
    });
    
    inputField.key('enter', () => {
        var text = inputField.getValue();
        text = text?.trim()
        if(text) sendMessage(text);
        inputField.clearValue();
        screen.render();
    })
    
    messageList.key(['escape', 'q', 'C-c'], () => {
        return process.exit(0)
    })
    
    screen.append(messageList);
    screen.append(inputField);
    inputField.focus();
    
    screen.render();
})
