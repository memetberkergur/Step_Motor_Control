#include <AccelStepper.h>

#define PULSE_PIN D5
#define DIRECTION_PIN D6
#define ENABLE_PIN D7

// Motor kontrolcüsünü tanımla
AccelStepper stepper(AccelStepper::DRIVER, PULSE_PIN, DIRECTION_PIN);

// Varsayılan ayarlar
long steps = 2880; // Varsayılan adım sayısı
float speed = 1000.0; // Varsayılan hız
float acceleration = 500.0; // Varsayılan ivme
float milimeter = 1.0;
int target_position = steps;
int direction = 1; // Varsayılan yön (1: ileri, -1: geri)

bool motorEnabled = false;

void setup() {
  Serial.begin(115200);
  
  stepper.setMaxSpeed(speed);
  stepper.setAcceleration(acceleration);
  
  // Varsayılan ayarları seri porttan yazdır
  Serial.println("\n\n\n\n\nStepper motor control initialized.");
  Serial.println("");
  Serial.println("Default settings:");
  Serial.println("-----------------");
  Serial.print("Speed       : "); Serial.println(speed);
  Serial.print("Acceleration: "); Serial.println(acceleration);
  Serial.print("Steps       : "); Serial.println(steps);
  Serial.print("Milimeter   : "); Serial.println(milimeter);
  Serial.print("Direction   : "); Serial.println(direction == 1 ? "Forward" : "Reverse");
  Serial.println("\nEnter commands in the format:");
  Serial.println("-------------------------------");
  Serial.println("SPD   <value>");
  Serial.println("ACC   <value>");
  Serial.println("STEPS <value>");
  Serial.println("DIR   <1 or -1>");
  Serial.println("MOVE  <value>");
  Serial.println("START to start the motor.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Başı ve sonundaki boşlukları kaldır

    if (command.startsWith("SPD ")) {
      speed = command.substring(4).toFloat();
      stepper.setMaxSpeed(speed);
      Serial.print("Speed set to: ");
      Serial.println(speed);
    } 
    else if (command.startsWith("ACC ")) {
      acceleration = command.substring(4).toFloat();
      stepper.setAcceleration(acceleration);
      Serial.print("Acceleration set to: ");
      Serial.println(acceleration);
    } 
    else if (command.startsWith("STEPS ")) {
      steps = command.substring(6).toInt();
      Serial.print("Steps set to: ");
      Serial.println(steps);
    } 
    else if (command.startsWith("DIR ")) {
      direction = command.substring(4).toInt();
      Serial.print("Direction set to: ");
      Serial.println(direction == 1 ? "Forward" : "Reverse");
    } 
    else if (command.startsWith("MOVE ")) {
      milimeter = command.substring(4).toFloat();
      target_position = milimeter * steps;
      Serial.print("Going to: ");
      Serial.print(milimeter);
      Serial.println("mm");
    } 
    else if (command.equals("START")) {
      motorEnabled = true;
      stepper.setCurrentPosition(0);
      stepper.moveTo(target_position*direction);
      Serial.println("Motor started.");
    }
  }

  if (motorEnabled) {
    if (stepper.distanceToGo() == 0) {
      Serial.println("Motor stopped and locked.");
      motorEnabled = false;
    } 
    else {
      stepper.run();
    }
  }
}
