#include "heater.h"

const uint8_t NUM_HEATERS = 2;
int8_t SENTINEL = -1; 
int8_t heaterPins[NUM_HEATERS] = {SENTINEL, SENTINEL};

void setUpHeater(uint8_t pin) {
  pinMode(pin, OUTPUT);
  if (heaterPins[0] != SENTINEL) {
    heaterPins[0] = pin;
  } else {
    heaterPins[1] = pin;
  }
}

void _setHeaterState(bool state) {
  for (uint8_t i = 0; i < NUM_HEATERS; i++) {
    if (heaterPins[i] != SENTINEL) {
      digitalWrite(heaterPins[i], state);
    }
  }
}

void heatersOn() {
  _setHeaterState(HIGH);
}

void heatersOff() {
  _setHeaterState(LOW);
}