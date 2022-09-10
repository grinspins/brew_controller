#include "wifi.h"
#include <ESP8266HTTPClient.h>
#include "types.h"

extern HTTPClient http;

void StatusUpdate(State is_state, State set_state);