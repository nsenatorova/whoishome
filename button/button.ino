#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

String serverName = "http://lemonl1me.pythonanywhere.com/trigger/123";

const int buttonPin = 25;
int lastButtonState = HIGH;   

void setup() {
  
  Serial.begin(115200); 
  
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.println("Pin 25 input mode set");
    
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected");
}

void loop() {
  int reading = digitalRead(buttonPin);
  
  if (reading != lastButtonState && reading == HIGH)  {
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

      String serverPath = serverName;
      
      http.begin(serverPath.c_str());
      
      int httpResponseCode = http.GET();
      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        Serial.print("Button: ");
        Serial.println(reading);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    
  }
  lastButtonState = reading;
}
