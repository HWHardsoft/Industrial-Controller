/*
 *  Test program for Industrial Feather equipped with Huzzah32 or similar
 *  Version 1.0
 *  Copyright (C) 2018  Hartmut Wendt  www.zihatec.de
 *  
 *  
 *  (based on sources of https://github.com/angeloc/simplemodbusng)
 *  
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/  

#include "SimpleModbusSlave.h"


/* This example code has 9 holding registers. 6 analogue inputs, 1 button, 1 digital output
   and 1 register to indicate errors encountered since started.
   Function 5 (write single coil) is not implemented so I'm using a whole register
   and function 16 to set the onboard Led on the Atmega328P.
   
   The modbus_update() method updates the holdingRegs register array and checks communication.

   Note:  
   The Arduino serial ring buffer is 128 bytes or 64 registers.
   Most of the time you will connect the arduino to a master via serial
   using a MAX485 or similar.
 
   In a function 3 request the master will attempt to read from your
   slave and since 5 bytes is already used for ID, FUNCTION, NO OF BYTES
   and two BYTES CRC the master can only request 122 bytes or 61 registers.
 
   In a function 16 request the master will attempt to write to your 
   slave and since a 9 bytes is already used for ID, FUNCTION, ADDRESS, 
   NO OF REGISTERS, NO OF BYTES and two BYTES CRC the master can only write
   118 bytes or 59 registers.
 
   Using the FTDI USB to Serial converter the maximum bytes you can send is limited 
   to its internal buffer which is 60 bytes or 30 unsigned int registers. 
 
   Thus:
 
   In a function 3 request the master will attempt to read from your
   slave and since 5 bytes is already used for ID, FUNCTION, NO OF BYTES
   and two BYTES CRC the master can only request 54 bytes or 27 registers.
 
   In a function 16 request the master will attempt to write to your 
   slave and since a 9 bytes is already used for ID, FUNCTION, ADDRESS, 
   NO OF REGISTERS, NO OF BYTES and two BYTES CRC the master can only write
   50 bytes or 25 registers.
 
   Since it is assumed that you will mostly use the Arduino to connect to a 
   master without using a USB to Serial converter the internal buffer is set
   the same as the Arduino Serial ring buffer which is 128 bytes.
*/
 

// Using the enum instruction allows for an easy method for adding and 
// removing registers. Doing it this way saves you #defining the size 
// of your slaves register array each time you want to add more registers
// and at a glimpse informs you of your slaves register layout.

// port expressions for ADC1 ... ADC5
const int ADC_PORTS[5] = {4, 35, 34, 36, 39};

//////////////// registers of your slave ///////////////////
enum 
{     
  // just add or remove registers and your good to go...
  // The first register starts at address 0    
  ADC1,        
  ADC2,
  ADC3,
  ADC4,
  ADC5,  
  LED_STATE,
  TOTAL_ERRORS,
  // leave this one
  TOTAL_REGS_SIZE 
  // total number of registers for function 3 and 16 share the same register array
};

byte ledState=0; // led off
int  errors=0;   // communication errors


unsigned int holdingRegs[TOTAL_REGS_SIZE]; // function 3 and 16 register array
////////////////////////////////////////////////////////////

void setup()
{
  // init UART0 for debugging
  Serial.begin(115200);

  /* parameters(long baudrate, 
                unsigned char ID, 
                unsigned char transmit enable pin, 
                unsigned int holding registers size,
                unsigned char low latency)
                
     The transmit enable pin is used in half duplex communication to activate a MAX485 or similar
     to deactivate this mode use any value < 2 because 0 & 1 is reserved for Rx & Tx.
     Low latency delays makes the implementation non-standard
     but practically it works with all major modbus master implementations.
  */  
  Serial.print("Init MODBUS..."); 
  modbus_configure(9600, 1, 14, TOTAL_REGS_SIZE, 0);
  Serial.println("done!"); 

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
    
}

void loop()
{
  // modbus_update() is the only method used in loop(). It returns the total error
  // count since the slave started. You don't have to use it but it's useful
  // for fault finding by the modbus master.
  holdingRegs[TOTAL_ERRORS] = modbus_update(holdingRegs);
  if (errors != holdingRegs[TOTAL_ERRORS]) {
    errors = holdingRegs[TOTAL_ERRORS];
    Serial.print("Errors: ");
    Serial.println(errors);    
  }  
  for (byte i = 0; i < 5; i++)
  {
    holdingRegs[i] = analogRead(ADC_PORTS[i]);
    delayMicroseconds(50);	     
  }

  
  // byte buttonState = digitalRead(buttonPin); // read button states
  
  // assign the buttonState value to the holding register
  //holdingRegs[BUTTON_STATE] = buttonState; 
  
  // read the LED_STATE register value and set the onboard LED high or low with function 16
  if (ledState != holdingRegs[LED_STATE]){
    ledState = holdingRegs[LED_STATE]; 
    
    if (ledState) // set led
    {		  
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      Serial.println("LED ON");
    }  
    else if (ledState == 0) // reset led
    {
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      Serial.println("LED OFF");
    }
  }
}
