#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "ESP8266TimerInterrupt.h"
#include <ESP8266HTTPClient.h>
#include "wifi.h"
#include "heater.h"

#define HEATER1_PIN 2
#define HEATER2_PIN 0
#define AC_FREQUENCY 50

typedef struct State {
  float temperature;
  bool pump_state;
} State;

volatile uint8_t gv_heater_duty_cycle = 0;
volatile uint8_t gv_heater_cycle_count = 0;
volatile State set_state = {
  .temperature = 0.0,
  .pump_state = false
};
volatile State is_state = {
  .temperature = 0.0,
  .pump_state = false
};
volatile HTTPClient http;

WiFiEventHandler gotIpEventHandler, disconnectedEventHandler;
ESP8266Timer ITimer;
WiFiClient client;


#define USE_SERIAL Serial

// TODO probably also put into heater.h
void setHeaTerDutyCycle(uint8_t duty_cycle) {
  if (duty_cycle % 2) {
    duty_cycle = duty_cycle - 1;
  }
  gv_heater_duty_cycle = duty_cycle;
}

void IRAM_ATTR TimerHandler()
{
  gv_heater_cycle_count++;
  const uint8_t cur_duty_cyle = gv_heater_cycle_count * 2;
  // Serial.println(cur_duty_cyle);
  if (cur_duty_cyle == gv_heater_duty_cycle) {
    heatersOff();
  } 
  if (cur_duty_cyle  == 100) {
    heatersOn();
    gv_heater_cycle_count = 0;
  }
}


void IRAM_ATTR StatusUpdate()
{
  uint8_t payload[5];
  payload[0] = is_state.temperature;
  payload[5] = (uint8_t) is_state.pump_state;
  int httpResponseCode = http.POST(payload, sizeof payload);
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString(); // Need to get bytes
  }
  http.end();
}


void setup() {
  setUpHeater(HEATER1_PIN);
  setUpHeater(HEATER2_PIN);

  gotIpEventHandler = WiFi.onStationModeGotIP([](const WiFiEventStationModeGotIP& event)
  {
    // event.ip has ip address
    heatersOn();
  });

  disconnectedEventHandler = WiFi.onStationModeDisconnected([](const WiFiEventStationModeDisconnected& event)
  {
    heatersOff();
  });

  connectWifi("papayaplaya", "Abbiefeia1!");
  // server address, port and URL
  USE_SERIAL.begin(115200);

	//Serial.setDebugOutput(true);
	USE_SERIAL.setDebugOutput(true);
    
  http.begin(client, "192.168.0.TODO");
  http.addHeader("Content-Type", "application/octet-stream");

  ITimer.attachInterrupt(AC_FREQUENCY, TimerHandler);
  ITimer.attachInterrupt(5, StatusUpdate);
}

void loop() {
 
}
