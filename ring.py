import serial
import time
import pygame

PORTA_BLUETOOTH = "COM9"
VELOCIDADE = 115200
pygame.mixer.init()

def conectar_serial():
    while True:
        try:
            BT = serial.Serial(PORTA_BLUETOOTH, VELOCIDADE, timeout=1)
            print("Conectado com sucesso!")
            return BT
        except serial.SerialException as e:
            print(f"Erro ao conectar: {e}. Tentando novamente...")
            time.sleep(2)

BT = conectar_serial()

while True:
    if BT:
        try:
            BT.write(b"ping")
            response = BT.readline().decode('utf-8').strip()
            if not response:
                raise serial.SerialException("Sem resposta do ESP32")
            print("Conexão ativa.")
            if BT and BT.in_waiting > 0:
                data = BT.readline().decode('utf-8').strip()
                print(f"Recebido: {data}")
                pygame.mixer.Sound("doorbell.mp3").play()
                
        except serial.SerialException:
            print("Conexão perdida! Fechando...")
            BT.close()
            BT = None

    if BT is None:
        try:
            BT = serial.Serial(PORTA_BLUETOOTH, VELOCIDADE, timeout=3)
            print("Reconectado!")

        except serial.SerialException:
            print("Aguardando reconexão...")

    time.sleep(0.1)
