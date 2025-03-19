#include <BluetoothSerial.h>

#define BUTTON_PIN 12

BluetoothSerial SerialBT;
bool button_pressed = false;
bool bt_connected = false;

void button_callback() {
  if (!button_pressed && digitalRead(BUTTON_PIN)) {
    button_pressed = true;
    SerialBT.println("DING");
  }
  if (button_pressed && !digitalRead(BUTTON_PIN)) {
    button_pressed = false;
  }
}

void check_bt_connection() {
  bool current_status = SerialBT.hasClient();

  if (bt_connected && !current_status) {
    Serial.println("⚠ Dispositivo desconectado! Reiniciando Bluetooth...");
    SerialBT.end();
    delay(1000);
    SerialBT.begin("Campainha");
  }

  if (!bt_connected && current_status) {
    Serial.println("🔵 Dispositivo conectado!");
  }

  bt_connected = current_status;
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLDOWN);
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);
  SerialBT.begin("Campainha");
  delay(100);
}

void loop() {
  if (SerialBT.available()) {
    String data = SerialBT.readString();
    data.trim();
    if (data == "ping") {
      SerialBT.println("pong");
    }
  }
  button_callback();
  delay(100);
}