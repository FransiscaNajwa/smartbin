#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// === Konfigurasi Pin ===
#define DHT_PIN 4
#define DHT_TYPE DHT11
#define TRIG_PIN 5
#define ECHO_PIN 18

DHT dht(DHT_PIN, DHT_TYPE);

// === WiFi ===
const char* ssid = "PES";
const char* password = "12345678";

// === MQTT ===
const char* mqtt_server = "broker.hivemq.com";   // Ganti dengan broker kamu jika ada
const int mqtt_port = 1883;
const char* mqtt_topic = "smartbin/data";

WiFiClient espClient;
PubSubClient client(espClient);

// === Variabel Sistem ===
const float DISTANCE_THRESHOLD = 10.0;
const unsigned long SEND_INTERVAL = 5000; // 5 detik
unsigned long lastSend = 0;
bool lastContainerStatus = false;

// === Deklarasi Fungsi ===
void connectToWiFi();
void reconnectMQTT();
void sendAllDataToMQTT();
float getDistance();
void triggerBuzzer();

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  // pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(TRIG_PIN, LOW);
  // digitalWrite(BUZZER_PIN, LOW);

  dht.begin();

  Serial.println("=== ESP32 Multi Sensor (MQTT Mode) ===");

  connectToWiFi();

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  // Pastikan koneksi WiFi tetap aktif
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  // Pastikan koneksi MQTT aktif
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Kirim data setiap 10 detik
  if (millis() - lastSend >= SEND_INTERVAL) {
    sendAllDataToMQTT();
    lastSend = millis();
  }

  delay(1000);
}

void connectToWiFi() {
  Serial.printf("\nMenghubungkan ke WiFi: %s\n", ssid);
  WiFi.begin(ssid, password);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi Terhubung!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ Gagal konek ke WiFi.");
  }
}

void reconnectMQTT() {
  // Loop hingga koneksi MQTT tersambung
  while (!client.connected()) {
    Serial.print("Menghubungkan ke broker MQTT...");
    String clientId = "ESP32-" + String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println(" ✓ Tersambung ke MQTT!");
      // Bisa menambahkan client.subscribe() di sini jika ingin menerima pesan
    } else {
      Serial.print(" ✗ Gagal, rc=");
      Serial.print(client.state());
      Serial.println(" | Coba lagi dalam 5 detik...");
      delay(5000);
    }
  }
}

void sendAllDataToMQTT() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float distance = getDistance();
  bool containerFull = (distance <= DISTANCE_THRESHOLD);

  // Format JSON
  String payload = "{";
  payload += "\"device_id\":\"bin001\",";
  payload += "\"temperature\":" + String(temperature, 2) + ",";
  payload += "\"humidity\":" + String(humidity, 2) + ",";
  payload += "\"distance\":" + String(distance, 2) + ",";
  payload += "\"status\":\"" + String(containerFull ? "penuh" : "kosong") + "\"";
  payload += "}";

  Serial.println("Mengirim data MQTT: " + payload);

  if (client.publish(mqtt_topic, payload.c_str())) {
    Serial.println("✓ Data berhasil dikirim ke broker!");
  } else {
    Serial.println("✗ Gagal mengirim data ke broker!");
  }
}

float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout

  if (duration > 0) {
    float distance = duration * 0.034 / 2;
    return distance;
  }

  return -1;
}
