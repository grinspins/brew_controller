#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "ESP8266TimerInterrupt.h"
#include "WebSocketsClient.h"
#include "wifi.h"
#include "heater.h"

#define HEATER1_PIN 2
#define HEATER2_PIN 0
#define AC_FREQUENCY 50

volatile uint8_t gv_heater_duty_cycle = 0;
volatile uint8_t gv_heater_cycle_count = 0;

WiFiEventHandler gotIpEventHandler, disconnectedEventHandler;
ESP8266Timer ITimer;
WebSocketsClient webSocket;

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

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

	switch(type) {
		case WStype_DISCONNECTED:
			USE_SERIAL.printf("[WSc] Disconnected!\n");
			break;
		case WStype_CONNECTED: {
			USE_SERIAL.printf("[WSc] Connected to url: %s\n", payload);

			// send message to server when Connected
			webSocket.sendTXT("Connected");
		}
			break;
		case WStype_TEXT:
			USE_SERIAL.printf("[WSc] get text: %s\n", payload);

			// send message to server
			// webSocket.sendTXT("message here");
			break;
		case WStype_BIN:
			USE_SERIAL.printf("[WSc] get binary length: %u\n", length);
			hexdump(payload, length);

			// send data to server
			// webSocket.sendBIN(payload, length);
			break;
    case WStype_PING:
        // pong will be send automatically
        USE_SERIAL.printf("[WSc] get ping\n");
        break;
    case WStype_PONG:
        // answer to a ping we send
        USE_SERIAL.printf("[WSc] get pong\n");
        break;
    }

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

	webSocket.begin("192.168.0.169", 8000, "/");

	// event handler
	webSocket.onEvent(webSocketEvent);

	// try ever 5000 again if connection has failed
	webSocket.setReconnectInterval(5000);
  
  // start heartbeat (optional)
  // ping server every 15000 ms
  // expect pong from server within 3000 ms
  // consider connection disconnected if pong is not received 2 times
  webSocket.enableHeartbeat(15000, 3000, 2);
  
  // ITimer.attachInterrupt(AC_FREQUENCY, TimerHandler);
  // ITimer.attachInterrupt(5, StatusUpdate);
  // setHeaTerDutyCycle(50);
}

void loop() {
  webSocket.loop();
}
