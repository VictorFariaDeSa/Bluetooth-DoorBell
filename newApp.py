import bluetooth
import time

ESP32_MAC = "14:2B:2F:EA:26:2E"  # Substitua pelo endereço MAC do ESP32
TIMEOUT = 5  # Tempo máximo sem mensagens antes de considerar desconexão

def conectar():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((ESP32_MAC, 1))  # Canal 1 geralmente é usado para BluetoothSerial
    sock.settimeout(TIMEOUT)  # Define o tempo limite para receber dados
    print("Conectado ao ESP32")
    return sock

try:
    sock = conectar()
    last_received = time.time()

    while True:
        try:
            data = sock.recv(1024).decode("utf-8").strip()
            if data:
                print(f"Recebido: {data}")
                last_received = time.time()  # Atualiza o tempo da última mensagem
            
            # Verifica se passou muito tempo sem receber mensagens
            if time.time() - last_received > TIMEOUT:
                print("Conexão perdida!")
                sock.close()
                sock = conectar()  # Tenta reconectar
                last_received = time.time()
        
        except bluetooth.BluetoothError:
            print("Erro na conexão, tentando reconectar...")
            sock.close()
            sock = conectar()
            last_received = time.time()

except KeyboardInterrupt:
    print("Finalizando conexão...")
    sock.close()
