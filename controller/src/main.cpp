#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "ESP8266TimerInterrupt.h"
#include <ESP8266HTTPClient.h>
#include <credentials.h>
#include "wifi.h"
#include "heater.h"

#define HEATER1_PIN 2
#define HEATER2_PIN 0
#define AC_FREQUENCY 50
#define POST_FREQUENCY 0.2
#define ssid ""

typedef struct State {
  float temperature;
  bool pump_state;
} State;

volatile uint8_t gv_heater_duty_cycle = 0;
volatile uint8_t gv_heater_cycle_count = 0;
volatile bool gv_do_post = false;

State set_state = {
  .temperature = 0.0,
  .pump_state = false
};
State is_state = {
  .temperature = 0.0,
  .pump_state = false
};

WiFiEventHandler gotIpEventHandler, disconnectedEventHandler;
ESP8266Timer ITimer;
WiFiClient client;
HTTPClient http;

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
  if (cur_duty_cyle == 100) {
    heatersOn();
    gv_heater_cycle_count = 0;
  }
}

void IRAM_ATTR EnablePost()
{
  gv_do_post = true;
}

void StatusUpdate()
{
  http.begin(client, "http://192.168.0.169:5000/mcu");
  http.addHeader("Content-Type", "application/octet-stream");
  uint8_t payload[5];
  memcpy(payload, &is_state.temperature, 4);
  payload[4] = (uint8_t) is_state.pump_state;
  int httpResponseCode = http.POST(payload, sizeof payload);
  if (httpResponseCode > 0) {
    String response = http.getString();
    memcpy(&set_state.temperature, &response, 4);
    set_state.pump_state = (bool) response[4];
  }
  http.end();
}


void setup() {
  setUpHeater(HEATER1_PIN);
  setUpHeater(HEATER2_PIN);

  gotIpEventHandler = WiFi.onStationModeGotIP([](const WiFiEventStationModeGotIP& event)
  {
    heatersOn();
  });

  disconnectedEventHandler = WiFi.onStationModeDisconnected([](const WiFiEventStationModeDisconnected& event)
  {
    heatersOff();
  });

  connectWifi(WIFI_SSID, WIFI_PW);
  Serial.begin(115200);

	Serial.setDebugOutput(true);
  ITimer.attachInterrupt(AC_FREQUENCY, TimerHandler);
  ITimer.attachInterrupt(POST_FREQUENCY, EnablePost);
}

void loop() {
  if (gv_do_post) {
    StatusUpdate();
    gv_do_post = false;
  }
  digitalWrite(HEATER1_PIN, set_state.pump_state);
  is_state.pump_state = set_state.pump_state;
}
