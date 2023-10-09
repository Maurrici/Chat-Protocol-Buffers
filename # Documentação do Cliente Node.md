# Documentação do Cliente Node.js

## Dependências
O cliente Node.js usa as seguintes bibliotecas:
- `protobufjs`: para serialização e desserialização de mensagens usando Protocol Buffers.
- `net`: para criar conexões de socket TCP.
- `readline-sync`: para ler a entrada do usuário no terminal.
- `neo-blessed`: para criar uma interface de usuário no terminal.

## Arquivos
O cliente consiste em dois arquivos principais: `index.js` e `chat.proto`.

### chat.proto
Este arquivo define as mensagens Protocol Buffers usadas na comunicação entre o cliente e o servidor. Ele define duas mensagens:

1. `ChatRequest`: Esta mensagem é usada quando o cliente faz uma solicitação ao servidor. Ela tem dois campos:
    - `action`: uma string que representa a ação que o cliente deseja realizar.
    - `value`: uma string que contém qualquer valor associado à ação.

2. `ChatMessage`: Esta mensagem é usada quando o servidor envia uma resposta ao cliente. Ela tem três campos:
    - `type`: uma string que representa o tipo da mensagem.
    - `userName`: uma string que representa o nome do usuário que enviou a mensagem.
    - `message`: uma string que contém a mensagem enviada pelo usuário.

### index.js
Este arquivo contém o código principal do cliente. Ele importa as dependências necessárias, carrega as definições de mensagens do Protocol Buffers, cria um socket TCP para se conectar ao servidor e define a lógica para lidar com as mensagens recebidas do servidor e enviar mensagens para o servidor.

#### Funções Principais
1. `createMessage(action, value)`: Esta função cria uma nova mensagem ChatRequest com a ação e valor fornecidos, verifica se a mensagem é válida e, em seguida, codifica a mensagem em um buffer antes de retorná-la.

2. `getObjectFromData(data)`: Esta função decodifica uma mensagem ChatMessage de um buffer e converte a mensagem em um objeto JavaScript.

3. `handleMessage(message)`: Esta função lida com as mensagens recebidas do servidor. Ela verifica o tipo da mensagem e realiza ações correspondentes.

4. `sendMessage(text)`: Esta função envia mensagens para o servidor. Ela verifica se a mensagem é uma ação especial (como "/USUARIOS", "/NICK", "/SAIR") e envia uma solicitação correspondente ao servidor.

#### Fluxo Principal
Quando o script é executado, ele pede ao usuário para inserir um apelido, cria um socket TCP para se conectar ao servidor e envia uma solicitação "/ENTRAR" ao servidor com o apelido do usuário. Em seguida, ele define manipuladores de eventos no socket para lidar com dados recebidos do servidor, erros de socket e fechamento de socket.

## Ações Especiais
Existem algumas ações especiais que o usuário pode realizar:
- `/USUARIOS`: Solicita ao servidor uma lista de usuários conectados.
- `/NICK <novo apelido>`: Solicita ao servidor para mudar o apelido do usuário.
- `/SAIR`: Solicita ao servidor para desconectar o usuário.

Espero que esta documentação seja útil para entender como funciona o cliente Node.js! Se você tiver alguma dúvida, não hesite em perguntar.