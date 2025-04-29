import serial
import time
import pygame



CHECK_TIMER = 5

class Receiver():
    def __init__(self,COM,baudRate):
        self.COM = COM
        self.baudRate = baudRate
        self.bt = None
        self.last_checked_time = time.time()
        self.counter = 0
        pygame.mixer.init()

    def connect_to_serial(self):
        while True:
            try:
                self.bt = serial.Serial(self.COM, self.baudRate, timeout=1)
                print("✅ Conectado com sucesso!")
                self.last_checked_time = time.time()
                break
            except serial.SerialException as e:
                print(f"❌ Erro ao conectar: {e}. Tentando novamente...")
                time.sleep(1)

    def play_song(self,path = "doorbell.mp3"):
        pygame.mixer.Sound(path).play()

    def ping_esp(self):
        self.counter = 0
        self.bt.write(b"ping\n")
        response = self.bt.readline().decode('utf-8').strip()
        if response == "DING":
            print("received")
            self.play_song()
            return 1
        if not response:
            return 0
        return 1

    def main_loop(self):
        check = 0
        if self.bt.in_waiting > 0:
                response = self.bt.readline().decode('utf-8').strip()
                print(response)
                print("received")
                self.play_song()
                check = 1
        if not check:
            check = self.ping_esp()
        if check:
                self.last_checked_time = time.time()
        elif time.time() - self.last_checked_time > CHECK_TIMER:                                   
            self.bt.close()
            self.connect_to_serial()
        

receiver = Receiver("COM9",115200)

receiver.connect_to_serial()
while True:
    receiver.main_loop()
