#include <BluetoothSerial.h>

#define BUTTON_PIN 12

BluetoothSerial SerialBT;
bool button_pressed = false;
bool bt_connected = false;
unsigned long last_check = 0;


void button_callback() {
  if (!button_pressed && digitalRead(BUTTON_PIN)) {
    button_pressed = true;
    SerialBT.println("DING");
  }
  if (button_pressed && !digitalRead(BUTTON_PIN)) {
    button_pressed = false;
  }
}

void restart_bt() {
  Serial.println("⚠ Dispositivo desconectado! Reiniciando Bluetooth...");
  SerialBT.end();
  delay(1000);
  SerialBT.begin("Campainha");
  delay(1000);
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLDOWN);
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);
  Serial.begin(115200);
  SerialBT.begin("Campainha");
  delay(100);
}

void loop() {
    if (!SerialBT.connected()) {
    Serial.println("Tentando reconectar...");
    SerialBT.begin("Campainha");
    delay(2000);
  }
  if (SerialBT.available()) {
    String data = SerialBT.readStringUntil('\n');
    data.trim();
    Serial.println(data);
    if (data == "ping") {
      SerialBT.println("pong");
      last_check = millis();
      bt_connected = true;
    }
  }

  button_callback();
  delay(100);
}