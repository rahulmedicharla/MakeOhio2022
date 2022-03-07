
// Include Libraries
#include "Arduino.h"
#include "DCMDriverL298.h"


// Pin Definitions
#define DCMOTORDRIVERL298_PIN_INT1	2
#define DCMOTORDRIVERL298_PIN_ENB	6
#define DCMOTORDRIVERL298_PIN_INT2	3
#define DCMOTORDRIVERL298_PIN_ENA	5
#define DCMOTORDRIVERL298_PIN_INT3	4
#define DCMOTORDRIVERL298_PIN_INT4	7

int piezoPin = 10;
int ledPin1 = 8;
int ledPin2 = 9;



// Global variables and defines

// object initialization
DCMDriverL298 dcMotorDriverL298(DCMOTORDRIVERL298_PIN_ENA,DCMOTORDRIVERL298_PIN_INT1,DCMOTORDRIVERL298_PIN_INT2,DCMOTORDRIVERL298_PIN_ENB,DCMOTORDRIVERL298_PIN_INT3,DCMOTORDRIVERL298_PIN_INT4);

// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    pinMode(ledPin1, OUTPUT);
    pinMode(ledPin2, OUTPUT);
    
}

// Main logic of your circuit. It defines the interaction between the components you selected. After setup, it runs over and over again, in an eternal loop.
void loop() 
{
  if(Serial.available() > 0){
    int key = Serial.read() - '0';
    Serial.print(key);
    Serial.print(" key Val");
    Serial.println();
    
    if(key == 0){
      dcMotorDriverL298.setMotorA(200,1);
      dcMotorDriverL298.setMotorB(200,0);
    } else if(key == 1){
       dcMotorDriverL298.setMotorA(50,1);
       dcMotorDriverL298.setMotorB(200,0);
    } else if(key ==2){
       dcMotorDriverL298.setMotorA(200,1);
      dcMotorDriverL298.setMotorB(50,0);
    }else if(key == 3){
      for(int i = 0; i < 3; i++){
        tone(piezoPin, 1000, 500);
        delay(1000);
      }
    }else if(key == 4){
      for(int i = 0; i < 5; i++){
        tone(piezoPin, 1500, 500);
        delay(500);
      }
    } else if(key == 5){
      dcMotorDriverL298.stopMotors();
      for(int i = 0; i < 5; i++){
        digitalWrite(ledPin1, HIGH);
        delay(1000);
        digitalWrite(ledPin1, LOW);
        digitalWrite(ledPin2, HIGH);
        delay(1000);
        digitalWrite(ledPin2, LOW);
      }
     digitalWrite(ledPin1,LOW);
    }

    delay(1000);
    
  }
}