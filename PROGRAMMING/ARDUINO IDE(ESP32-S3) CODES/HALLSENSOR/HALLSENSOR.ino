#include <Arduino.h>

// Define pins
#define AUX 4
#define TX 42
#define RX 41
#define M1 48
#define M0 45

// HardwareSerial can be used on ESP32 instead of SoftwareSerial for better reliability
HardwareSerial LoraSerial(2);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("E32 LoRa Receiver Starting...");

  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(AUX, INPUT);

  // Set LoRa module to normal mode (M0=0, M1=0)
  digitalWrite(M0, LOW);
  digitalWrite(M1, LOW);

  // Initialize Serial1 with RX/TX pins
  LoraSerial.begin(9600, SERIAL_8N1, RX, TX);

  // Wait for module to be ready
  unsigned long start = millis();
while (digitalRead(AUX) == LOW && millis() - start < 2000);

  delay(100);
  Serial.println("LoRa Module Ready. Waiting for data...");
}

void loop() {
  if (LoraSerial.available()) {
    String incoming = "";
    while (LoraSerial.available()) {
      char c = LoraSerial.read();
      incoming += c;
    }

    Serial.print("Received: ");
    Serial.println(incoming);
  }
}
