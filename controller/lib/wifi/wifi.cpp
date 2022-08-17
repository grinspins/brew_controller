#include "wifi.h"

void connectWifi(const String ssid, const String password) {
  WiFi.begin("papayaplaya", "Abbiefeia1!");

  while (WiFi.status() != WL_CONNECTED)
  {
      delay(500);
  }
};
  