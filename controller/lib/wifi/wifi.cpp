#include "wifi.h"

WiFiClient client;
WiFiEventHandler disconnectedEventHandler;

void connectWifi(const String ssid, const String password) {
  disconnectedEventHandler = WiFi.onStationModeDisconnected([](const WiFiEventStationModeDisconnected& event)
  {
    // TODO proper shutdown code
    heatersOff();
  });
  WiFi.begin("papayaplaya", "Abbiefeia1!");

  while (WiFi.status() != WL_CONNECTED)
  {
      delay(500);
  }
};
  