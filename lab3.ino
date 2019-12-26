#include <Servo.h>

Servo servo;
const int echoPin = 8;
const int trigPin = 9;

void setup() {
 servo.attach(10);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  digitalWrite(trigPin, LOW);
  Serial.begin(115200);
}

void loop() {
  
    for (int i = 0; i <= 180; i++) {
      servo.write(i);
      float result = readDist();
      Serial.println(String(i) + ' ' + String(result));
      delay(15);
    }
    for (int i = 180; i >= 0; i--) {
      servo.write(i);
      float result = readDist();
      Serial.println(String(i) + ' ' + String(result));
      delay(15);
    }
}

float readDist()
{
  const float speedOfSoundMPerSec = 340.0;
  const float speedOfSoundCmPerUs = speedOfSoundMPerSec / 10000.0;
  return readPulse() * speedOfSoundCmPerUs / 2.0;    
}

float readPulse()
{
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);

  return duration;
}
