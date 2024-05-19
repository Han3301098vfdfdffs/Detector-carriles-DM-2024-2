#include <ESP32Servo.h>
const int IN1pin = 12;
const int IN2pin = 13;
const int IN3pin = 5;
const int IN4pin = 16;
const int ENApin = 14;
const int ENBpin = 17;

int IN1, IN2, ENA, ENB, ServoValue;
TaskHandle_t Tarea1;  // Tarea1 Control Motor DC1
TaskHandle_t Tarea2;  // Tarea2 Control Motor DC2
TaskHandle_t Tarea3;  // Tarea3 Control Servo
Servo servoMotor;

void setup() {
  Serial.begin(115200);
  xTaskCreatePinnedToCore(loop1, "Tarea_1", 1000, NULL, 1, &Tarea1, 0);
  xTaskCreatePinnedToCore(loop2, "Tarea_2", 1000, NULL, 1, &Tarea2, 0);
  xTaskCreatePinnedToCore(loop3, "Tarea_3", 1000, NULL, 1, &Tarea3, 1);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    parseInput(input);
  }
}

void parseInput(String input) {
  char* token = strtok(const_cast<char*>(input.c_str()), ":"); 

  if (token != NULL) {
    IN1 = atoi(token);  
    token = strtok(NULL, ":");  

    if (token != NULL) {
      IN2 = atoi(token);
      token = strtok(NULL, ":");

      if (token != NULL) {
        ENA = atoi(token);
        token = strtok(NULL, ":");

        if (token != NULL) {
          ENB = atoi(token);
          token = strtok(NULL, ":");

          if (token != NULL) {
            ServoValue = atoi(token);
            token = strtok(NULL, ":");
          }
        }
      }
    }
  }
  updatePins();
}

void updatePins() {
  pinMode(IN1pin, OUTPUT);
  pinMode(IN2pin, OUTPUT);
  pinMode(IN3pin, OUTPUT);
  pinMode(IN4pin, OUTPUT);
  pinMode(ENApin, OUTPUT);
  pinMode(ENBpin, OUTPUT);
  servoMotor.attach(4);
}

void loop1(void *parameter) {  
  while (true) {
    digitalWrite(IN1pin, IN1);
    digitalWrite(IN2pin, IN2);
    analogWrite(ENApin, ENA);  
    delay(10);
  }
}

void loop2(void *parameter) {  
  while (true) {
    digitalWrite(IN3pin, IN1);
    digitalWrite(IN4pin, IN2);
    analogWrite(ENBpin, ENB);  
    delay(10);
  }
}

void loop3(void *parameter) {  
  while (true) {
    servoMotor.write(ServoValue);   
    delay(10);
  }
}
