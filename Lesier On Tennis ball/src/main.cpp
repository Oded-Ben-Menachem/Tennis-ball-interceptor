#include <Arduino.h>
#include <ESP32Servo.h>

Servo Horizontal;
Servo Vertical;

const int horiPin = 25;
const int verPin = 33;
const int laserPin = 26;


void setup() {

    Serial.begin(115200);

    pinMode(laserPin, OUTPUT);

    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);

    Horizontal.setPeriodHertz(50);
    Vertical.setPeriodHertz(50);

    Horizontal.attach(horiPin, 500, 2400);
    Vertical.attach(verPin, 500, 2400);



    Serial.println("Servos Initialized!");



    Horizontal.write(90);
    Vertical.write(90);

}



void loop() {

  delay(2000);

  digitalWrite(laserPin,HIGH);

  //Horizontal.write(99);

  //Vertical.write(99);

  delay(3000);

  digitalWrite(laserPin,LOW);

  //Horizontal.write(90);

  //Vertical.write(90);

  //delay(10000);

 

 

}