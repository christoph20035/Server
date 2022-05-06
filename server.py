import socket 
import threading

#threading zorgt ervoor dat je niet hoeft te wachten op een stap voor de volgende stap
HEADER = 64
PORT = 9999
#locaal
#SERVER = socket.gethostbyname(socket.gethostname()) #zoek het ip adres van dit apparaat

#via internet
SERVER = '127.0.0.1'

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_inet is het type adres wat we zoeken
print(ADDR)
server.bind(ADDR) #alle informatie gaat gefilterd worden denk ik

def handle_client(conn, addr): #hier wordt elke connectie gecontroleerd en verwerkt
    print(f'[NEW CONNECTION] {addr} connected.') #wie is verbonden

    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)   #deze stap zal pas verder gaan indien het programma data ontvangt
        if msg_length:                                                #de recv functie moet gevuld worden met een bepaald aantal bites dus eerst gaan we de client een 64 bits cijfer laten sturen wat de bites van de data zal gaan voorstellen
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'[{addr}] {msg}')

            conn.send('Msg received'.encode(FORMAT))

    conn.close()


def start(): #dit is voor de connecties binnen te krijgen en ze te verwerken
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr)) #dit zal handle_client starten en zal als argumenten conn en addr sturen
        thread.start()
        
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}') #dit zal weergeven hoeveel threads aant werken zijn dus hier uit wordt het aantal verbonden clients geteld


print("[STARTING] server is starting...")
start()