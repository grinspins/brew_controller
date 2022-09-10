#include "http.h"

HTTPClient http;

void StatusUpdate(State is_state, State set_state)
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