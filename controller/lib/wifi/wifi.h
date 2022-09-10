#include <ESP8266WiFi.h>
#include "heater.h"

extern WiFiClient client;
extern WiFiEventHandler disconnectedEventHandler;

void connectWifi(const String ssid, const String password);