// References:
// https://forum.arduino.cc/t/multiple-pwm-signal-reading-on-arduino-mega-2560/100257/6 : Reading PWM data from receiver
// https://forum.arduino.cc/t/determine-device-at-build-time/145824: Determining build device with preprocessor
// https://docs.arduino.cc/retired/hacking/software/PortManipulation/: Register information for Uno

#include <Servo.h>

#define RX_SERVO_PIN 2
#define RX_MOTOR_PIN 3
#define ESC_PIN 5
#define SERVO_PIN 6

// Controls how hard the car should brake. From 0 to 255.
#define E_BRAKE_POWER 255

// Max time between inputs until failsafe (milliseconds)
#define TIMEOUT 1000

// min and max values from RPI
#define MIN -255
#define MAX 255

// minimum and maximum pulse length
#define SERVO_MIN 1000
#define SERVO_MAX 2000

//PREPROCESSOR CHECKS

// Faster than digitalRead, might remove later
#if defined(__AVR_ATmega328P__)
  #define SERVO_REG (PIND & 0b0000100)
  #define MOTOR_REG (PIND & 0b0001000)
#elif defined(__AVR_ATmega2560__)
  #define SERVO_REG (PINE & 0x10)
  #define MOTOR_REG (PINE & 0x20)
#else
  #error "Invalid device configuration."
#endif

#if (E_BRAKE_POWER < 0 || E_BRAKE_POWER > 255)
  #error "Invalid value for E_BRAKE_POWER"
#endif


volatile unsigned long rx_servo_val;  // servo value
volatile unsigned long servo_count;     // temporary variable for servo PWM

volatile unsigned long rx_motor_val;  // servo value
volatile unsigned long motor_count;   // temporary variable for motor PWM

Servo servo;
Servo esc;

void setup() {
  Serial.begin(9600);

  servo.attach(SERVO_PIN);  // servo pin
  esc.attach(ESC_PIN);      // motor pin

  pinMode(RX_SERVO_PIN, INPUT);  // Rx servo pin
  pinMode(RX_MOTOR_PIN, INPUT);  // Rx motor pin

  attachInterrupt(digitalPinToInterrupt(RX_SERVO_PIN), handleInterrupt_Servo, CHANGE);  // Catch up and down
  attachInterrupt(digitalPinToInterrupt(RX_MOTOR_PIN), handleInterrupt_Motor, CHANGE);  // Catch up and down
}

int16_t motor_value = 0;
int16_t servo_value = 0;
uint32_t last_update = 0;
bool failsafe = true;
bool running = false;  // TODO: set to false once code is safe

void loop() {
  /* 
    TODO: Timeout should only run and print while bot is running; Should be reset and begin countdown when running becomes true, and stop or ignore when running becomes false
    TODO: SHOULD ONLY ARM if the bot was in the DISARMED state first (Test when migrating to another controller)
    TODO: After starting, should WIPE serial cache before accepting more input, and should disregard all but the newest line
  */

  // Needs to be changed to be latching maybe
  if (!running && rx_motor_val > 1950) {
    running = true;
    Serial.println("START");
  }

  if (running && rx_motor_val < 1200) {
    running = false;
    failsafe = true;
    //servo.writeMicroseconds(convertToPulseLength(0));
    // Brakes at half speed
    esc.writeMicroseconds(convertToPulseLength(-E_BRAKE_POWER));
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
      motor_value = data.substring(0, delim_index).toInt();
      servo_value = data.substring(delim_index + 1, data.length()).toInt();
      servo.writeMicroseconds(convertToPulseLength(servo_value));
      esc.writeMicroseconds(convertToPulseLength(motor_value));
      failsafe = false;
    } else Serial.println("ERROR");
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

void handleInterrupt_Servo() {
  if (SERVO_REG) servo_count = micros();       // we got a positive edge
  else rx_servo_val = micros() - servo_count;  // Negative edge: get pulsewidth
}

void handleInterrupt_Motor() {
  if (MOTOR_REG) motor_count = micros();       // we got a positive edge
  else rx_motor_val = micros() - motor_count;  // Negative edge: get pulsewidth
}

int16_t convertToPulseLength(int16_t value) {
  return constrain( map( value, MIN, MAX, SERVO_MIN, SERVO_MAX ), SERVO_MIN, SERVO_MAX);
}
