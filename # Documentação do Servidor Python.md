# Documentação do Servidor Python

## Dependências
O servidor Python usa as seguintes bibliotecas:
- `chat_pb2`: para serialização e desserialização de mensagens usando Protocol Buffers.
- `socket`: para criar conexões de socket TCP.
- `time`: para manipular o tempo.
- `threading`: para criar threads.

## Arquivos
O servidor consiste em dois arquivos principais: `index.py` e `chat.proto`.

### chat.proto
Este arquivo define as mensagens Protocol Buffers usadas na comunicação entre o cliente e o servidor. Ele define duas mensagens:

1. `ChatRequest`: Esta mensagem é usada quando o cliente faz uma solicitação ao servidor. Ela tem dois campos:
    - `action`: uma string que representa a ação que o cliente deseja realizar.
    - `value`: uma string que contém qualquer valor associado à ação.

2. `ChatMessage`: Esta mensagem é usada quando o servidor envia uma resposta ao cliente. Ela tem três campos:
    - `type`: uma string que representa o tipo da mensagem.
    - `userName`: uma string que representa o nome do usuário que enviou a mensagem.
    - `message`: uma string que contém a mensagem enviada pelo usuário.

### index.py
Este arquivo contém o código principal do servidor. Ele importa as dependências necessárias, carrega as definições de mensagens do Protocol Buffers, cria um socket TCP para aceitar conexões de clientes e define a lógica para lidar com as mensagens recebidas dos clientes e enviar mensagens para os clientes.

#### Funções Principais
1. `createMessage(type, userName, message)`: Esta função cria uma nova mensagem ChatMessage com o tipo, nome do usuário e mensagem fornecidos, e então codifica a mensagem em um buffer antes de retorná-la.

2. `getObjectFromData(data)`: Esta função decodifica uma mensagem ChatRequest de um buffer.

3. `handle_client(con, cliente)`: Esta função é executada em uma nova thread para cada cliente conectado. Ela lida com as mensagens recebidas do cliente e realiza ações correspondentes.

#### Fluxo Principal
Quando o script é executado, ele cria um socket TCP para aceitar conexões de clientes e entra em um loop infinito onde aceita novas conexões de clientes. Para cada nova conexão, ele inicia uma nova thread que executa a função handle_client.

## Ações Especiais
Existem algumas ações especiais que o cliente pode solicitar:
- `/ENTRAR`: Solicita ao servidor para entrar no chat.
- `/MENSAGEM`: Envia uma mensagem para todos os usuários no chat.
- `/USUARIOS`: Solicita ao servidor uma lista de usuários conectados.
- `/NICK <novo apelido>`: Solicita ao servidor para mudar o apelido do usuário.
- `/SAIR`: Solicita ao servidor para desconectar o usuário.

Espero que esta documentação seja útil para entender como funciona o servidor Python! Se você tiver alguma dúvida, não hesite em perguntar.