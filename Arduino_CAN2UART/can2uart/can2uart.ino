/* CAN Loopback Example
 * This example sends a message once a second and receives that message
 *   no CAN bus is required.  This example will test the functionality 
 *   of the protocol controller, and connections to it.
 *   
 *   Written By: Cory J. Fowler - October 5th 2016
 */

#include <mcp_can.h>
#include <SPI.h>
#include <ArduinoJson.h>

StaticJsonBuffer<200> jsonBuffer;

JsonObject& root = jsonBuffer.createObject();
JsonArray& data = root.createNestedArray("data");

// CAN TX Variables
unsigned long prevTX = 0;                                        // Variable to store last execution time
const unsigned int invlTX = 1000;                                // One second interval constant
byte data_buf[] = {0xAA, 0x55, 0x01, 0x10, 0xFF, 0x12, 0x34, 0x56};  // Generic CAN data to send

// CAN RX Variables
long unsigned int rxId;
unsigned char len;
unsigned char rxBuf[8];

// Serial Output String Buffer
char msgString[128];

// CAN0 INT and CS
#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10


void setup()
{
  Serial.begin(115200);  // CAN is running at 500,000BPS; 115,200BPS is SLOW, not FAST, thus 9600 is crippling.
  Serial1.begin(57600);
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  // Since we do not set NORMAL mode, we are in loopback mode by default.
  CAN0.setMode(MCP_NORMAL);

  pinMode(CAN0_INT, INPUT);                           // Configuring pin for /INT input

  for(byte i = 0; i<8; i++){
        data.add(0);
  }
//  Serial.println("MCP2515 Library Loopback Example...");
}

void loop()
{
  if(!digitalRead(CAN0_INT))                          // If CAN0_INT pin is low, read receive buffer
  {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);              // Read data: len = data length, buf = data byte(s)
    
    if((rxId & 0x80000000) == 0x80000000)             // Determine if ID is standard (11 bits) or extended (29 bits)
      sprintf(msgString, "Extended ID: 0x%.8lX  DLC: %1d  Data:", (rxId & 0x1FFFFFFF), len);
    else
    {
      sprintf(msgString, "Standard ID: 0x%.3lX       DLC: %1d  Data:", rxId, len);
      root.set<>("SubBoard_ID",rxId);
      root.set<>("data_len",len);
    }
  
//    Serial.print(msgString);
  
    if((rxId & 0x40000000) == 0x40000000){            // Determine if message is a remote request frame.
      sprintf(msgString, " REMOTE REQUEST FRAME");
      Serial.print(msgString);
    } else {
      for(byte i = 0; i<len; i++){
        data.set(i,rxBuf[i]);

//        sprintf(msgString, " 0x%.2X", rxBuf[i]);
//        Serial.print(msgString);
      }
    }
        
    Serial.println();
    root.printTo(Serial1);
    root.printTo(Serial);
    Serial1.println();
  }
  
//  if(millis() - prevTX >= invlTX){                    // Send this at a one second interval. 
//    prevTX = millis();
//    byte sndStat = CAN0.sendMsgBuf(0x100, 8, data_buf);
//    
//    if(sndStat == CAN_OK)
//      Serial.println("Message Sent Successfully!");
//    else
//      Serial.println("Error Sending Message...");
//
//  }
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
