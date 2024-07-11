// References:
// https://forum.arduino.cc/t/multiple-pwm-signal-reading-on-arduino-mega-2560/100257/6 : Reading PWM data from receiver

#include <Servo.h>

#define RX_SERVO_PIN  2
#define RX_MOTOR_PIN  3
#define SERVO_PIN     5
#define ESC_PIN       6

#define TIMEOUT 1000

// min and max values from RPI
#define MIN -255
#define MAX 255

// minimum and maximum pulse length
#define SERVO_MIN 1000
#define SERVO_MAX 2000

// PIN 2
#define int0 (PINE & 0x10) // #define int0 (PINE & 0b00010000) // Faster than digitalRead

// PIN 3
// #define int0 (PINE & 0b00100000)
#define int1 (PINE & 0x20)

volatile unsigned long rx_servo_val; // servo value
volatile unsigned long count0; // temporary variable for servo PWM

volatile unsigned long rx_motor_val; // servo value
volatile unsigned long count1; // temporary variable for motor PWM

Servo servo;
Servo esc;

void setup()
{
  Serial.begin(9600);

  servo.attach(SERVO_PIN); // servo pin
  esc.attach(ESC_PIN);   // motor pin

  pinMode(RX_SERVO_PIN,INPUT); // Rx servo pin
  pinMode(RX_MOTOR_PIN,INPUT); // Rx motor pin

  attachInterrupt(digitalPinToInterrupt(RX_SERVO_PIN), handleInterrupt_Servo, CHANGE); // Catch up and down
  attachInterrupt(digitalPinToInterrupt(RX_MOTOR_PIN), handleInterrupt_Motor, CHANGE); // Catch up and down
}

int16_t motor_value = 0;
int16_t servo_value = 0;
uint32_t last_update = 0;
bool failsafe = true;
bool running = false; // TODO: set to false once code is safe

void loop() {
  if (!running && rx_motor_val > 1950) {
    running = true;
    Serial.println("START");
  }

  if (running && rx_motor_val < 1200) {
    running = false;
    failsafe = true;
    //servo.writeMicroseconds(convertToPulseLength(0));
    esc.writeMicroseconds(convertToPulseLength(0));
    Serial.println("STOP");
  }

  // READ SERIAL
  if (running && Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    /*
    Serial.print("Data: ");
    Serial.println(data);
    */
    int delim_index = data.indexOf(',');
    
    // Input must have a comma in the middle somewhere
    if (delim_index > 0 && delim_index != data.length() - 1) {
      last_update = millis();

      // TODO: Data must be a valid int and in range before using
      servo_value = data.substring(0, delim_index).toInt();
      motor_value = data.substring(delim_index + 1, data.length()).toInt();
      servo.writeMicroseconds(convertToPulseLength(servo_value));
      esc.writeMicroseconds(convertToPulseLength(motor_value));
      failsafe = false;
    }
    else Serial.println("ERROR");
  }

  // No data detected in timespan, activating failsafe
  if (!failsafe && millis() >= last_update + TIMEOUT) {
    Serial.println("FAILSAFE");
    // Servo should keep its position
    //servo.writeMicroseconds(convertToPulseLength(0));
    esc.writeMicroseconds(convertToPulseLength(0));
    failsafe = true;
  }
  //if (!running && rx_motor_va)

  delay(10);
}

void handleInterrupt_Servo()
{
  if(int0)  count0 = micros(); // we got a positive edge
  else      rx_servo_val = micros() - count0; // Negative edge: get pulsewidth
}

void handleInterrupt_Motor()
{
  if(int1)  count1 = micros(); // we got a positive edge
  else      rx_motor_val = micros() - count1; // Negative edge: get pulsewidth
}

int16_t convertToPulseLength(int16_t value) {
  return min( max( map( value, MIN, MAX, SERVO_MIN, SERVO_MAX ), SERVO_MIN ), SERVO_MAX );
}
