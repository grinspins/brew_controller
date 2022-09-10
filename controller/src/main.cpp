#include <Arduino.h>
#include "ESP8266TimerInterrupt.h"
#include <Adafruit_MAX31865.h>
#include <Wire.h>
#include <credentials.h>
#include "heater.h"
#include "http.h"

#define HEATER1_PIN 2
#define HEATER2_PIN 0
#define AC_FREQUENCY 50
#define POST_FREQUENCY 0.2
#define CS_PIN 15
#define PT_100_RREF 430.0
#define PT_100_RNOMINAL 100.0

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

ESP8266Timer ITimer;
Adafruit_MAX31865 pt100 = Adafruit_MAX31865(CS_PIN);

// TODO probably also put into heater.h
void setHeaTerDutyCycle(uint8_t duty_cycle) {
  if (duty_cycle % 2) {
    duty_cycle = duty_cycle - 1;
  }
  gv_heater_duty_cycle = duty_cycle;
}

void IRAM_ATTR SSRHandler()
{
  gv_heater_cycle_count++;
  const uint8_t cur_duty_cyle = gv_heater_cycle_count * 2;
  if (cur_duty_cyle == gv_heater_duty_cycle) {
    heatersOff();
  } 
  if (cur_duty_cyle == 100) {
    heatersOn();
    gv_heater_cycle_count = 0;
  }
}

void IRAM_ATTR PostEnabler()
{
  gv_do_post = true;
}


void setup() {
  setUpHeater(HEATER1_PIN);
  setUpHeater(HEATER2_PIN);

  connectWifi(WIFI_SSID, WIFI_PW);
  // Serial.begin(115200);
	// Serial.setDebugOutput(true);
  pt100.begin(MAX31865_3WIRE);

  ITimer.attachInterrupt(AC_FREQUENCY, SSRHandler);
  ITimer.attachInterrupt(POST_FREQUENCY, PostEnabler);
}

void loop() {
  if (gv_do_post) {
    StatusUpdate(is_state, set_state);
    gv_do_post = false;
  }

  digitalWrite(HEATER1_PIN, set_state.pump_state);
  is_state.pump_state = set_state.pump_state;
  is_state.temperature = pt100.temperature(PT_100_RNOMINAL, PT_100_RREF);  
}
