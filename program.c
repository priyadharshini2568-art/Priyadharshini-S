#include <ESP8266WiFi.h>
#include <DHT.h>

WiFiClient client;
WiFiServer server(80);

/* WIFI settings */
const char* ssid = "TP-Link_8E98";
const char* password = "86427920";
String data = "";

/* Pin Definitions */
#define Relay1 D1    // FAN
#define Relay2 D2    // LIGHT
#define Relay3 D3
#define Relay4 D4
#define PIR_PIN D6    
#define DHT_PIN D5  
#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

const float TEMP_MIN = 25.0; // Fan won't turn on below 25°C

void setup() {
  pinMode(Relay1, OUTPUT); pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT); pinMode(Relay4, OUTPUT);
  pinMode(PIR_PIN, INPUT);
 
  // Set Relays OFF (High)
  digitalWrite(Relay1, HIGH); digitalWrite(Relay2, HIGH);
  digitalWrite(Relay3, HIGH); digitalWrite(Relay4, HIGH);
 
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  server.begin();
}

void loop() {
  client = server.available();
  if (!client) return;

  data = checkClient();
 
  if (data.length() > 0) {
    // FAN Logic: Check DHT11 before switching ON
    if (data == "r1on") {
      float currentTemp = dht.readTemperature();
      if (currentTemp >= TEMP_MIN) {
        digitalWrite(Relay1, LOW);
      }
    }
    else if (data == "r1off") digitalWrite(Relay1, HIGH);

    // LIGHT Logic: Check PIR before switching ON
    else if (data == "r2on") {
      if (digitalRead(PIR_PIN) == HIGH) {
        digitalWrite(Relay2, LOW);
      }
    }
    else if (data == "r2off") digitalWrite(Relay2, HIGH);

    // Other Relays (No sensor checks)
    else if (data == "r3on")  digitalWrite(Relay3, LOW);
    else if (data == "r3off") digitalWrite(Relay3, HIGH);
    else if (data == "r4on")  digitalWrite(Relay4, LOW);
    else if (data == "r4off") digitalWrite(Relay4, HIGH);
    else if (data == "allon") {
        // Only turns on Fan/Light if sensors allow
        if(dht.readTemperature() >= TEMP_MIN) digitalWrite(Relay1, LOW);
        if(digitalRead(PIR_PIN) == HIGH) digitalWrite(Relay2, LOW);
        digitalWrite(Relay3, LOW);
        digitalWrite(Relay4, LOW);
    }
    else if (data == "alloff") {
        digitalWrite(Relay1, HIGH); digitalWrite(Relay2, HIGH);
        digitalWrite(Relay3, HIGH); digitalWrite(Relay4, HIGH);
    }
   
    sendSimpleEcho(data);
  }
  data = "";
}

#include <ESP8266WiFi.h>
#include <DHT.h>

WiFiClient client;
WiFiServer server(80);

/* WIFI settings */
const char* ssid = "TP-Link_8E98";
const char* password = "86427920";
String data = "";

/* Pin Definitions */
#define Relay1 D1    // FAN
#define Relay2 D2    // LIGHT
#define Relay3 D3
#define Relay4 D4
#define PIR_PIN D6    
#define DHT_PIN D5  
#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

const float TEMP_MIN = 25.0; // Fan won't turn on below 25°C

void setup() {
  pinMode(Relay1, OUTPUT); pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT); pinMode(Relay4, OUTPUT);
  pinMode(PIR_PIN, INPUT);
 
  // Set Relays OFF (High)
  digitalWrite(Relay1, HIGH); digitalWrite(Relay2, HIGH);
  digitalWrite(Relay3, HIGH); digitalWrite(Relay4, HIGH);
 
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  server.begin();
}

void loop() {
  client = server.available();
  if (!client) return;

  data = checkClient();
 
  if (data.length() > 0) {
    // FAN Logic: Check DHT11 before switching ON
    if (data == "r1on") {
      float currentTemp = dht.readTemperature();
      if (currentTemp >= TEMP_MIN) {
        digitalWrite(Relay1, LOW);
      }
    }
    else if (data == "r1off") digitalWrite(Relay1, HIGH);

    // LIGHT Logic: Check PIR before switching ON
    else if (data == "r2on") {
      if (digitalRead(PIR_PIN) == HIGH) {
        digitalWrite(Relay2, LOW);
      }
    }
    else if (data == "r2off") digitalWrite(Relay2, HIGH);

    // Other Relays (No sensor checks)
    else if (data == "r3on")  digitalWrite(Relay3, LOW);
    else if (data == "r3off") digitalWrite(Relay3, HIGH);
    else if (data == "r4on")  digitalWrite(Relay4, LOW);
    else if (data == "r4off") digitalWrite(Relay4, HIGH);
    else if (data == "allon") {
        // Only turns on Fan/Light if sensors allow
        if(dht.readTemperature() >= TEMP_MIN) digitalWrite(Relay1, LOW);
        if(digitalRead(PIR_PIN) == HIGH) digitalWrite(Relay2, LOW);
        digitalWrite(Relay3, LOW);
        digitalWrite(Relay4, LOW);
    }
    else if (data == "alloff") {
        digitalWrite(Relay1, HIGH); digitalWrite(Relay2, HIGH);
        digitalWrite(Relay3, HIGH); digitalWrite(Relay4, HIGH);
    }
   
    sendSimpleEcho(data);
  }
  data = "";
}

String checkClient() {
  while(!client.available()) delay(1);
  String request = client.readStringUntil('\r');
  client.flush();
  int start = request.indexOf("/") + 1;
  int end = request.indexOf(" ", start);
  return request.substring(start, end);
}

void sendSimpleEcho(String echo) {
  client.println("HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html>OK</html>");
  delay(1);
  client.stop();
}
