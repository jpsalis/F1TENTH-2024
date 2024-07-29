// References:
// https://forum.arduino.cc/t/multiple-pwm-signal-reading-on-arduino-mega-2560/100257/6 : Reading PWM data from receiver
// https://forum.arduino.cc/t/determine-device-at-build-time/145824: Determining build device with preprocessor
// https://docs.arduino.cc/retired/hacking/software/PortManipulation/: Register information for Uno

/* Reads serial commands from main computer, and responds accordingly. Has various safety checks built-in. */
#include <Servo.h>

// Max time between inputs until failsafe (ms)
#define TIMEOUT 1000
// Time until robot can arm
#define PWR_ON_ARM_GRACE 2000

// Controls how hard the car should brake. From 0 to 255.
#define E_BRAKE_POWER 255
#define FAILSAFE_BRAKE_POWER 0

// min and max values from RPI
#define MIN -255
#define MAX 255

// minimum and maximum pulse length (μs)
#define SERVO_MIN 1000
#define SERVO_MAX 2000

// Pinouts
const int RX_SERVO_PIN = 2;
const int RX_MOTOR_PIN = 3;
const int ESC_PIN = 5;
const int SERVO_PIN = 6;
const int LED = LED_BUILTIN;

/* PREPROCESSOR CHECKS */

// Faster than digitalRead, used to read receiver. Might remove later
#if defined(__AVR_ATmega328P__)
  #define SERVO_REG (PIND & 0b0000100)
  #define MOTOR_REG (PIND & 0b0001000)
#elif defined(__AVR_ATmega2560__)
  #define SERVO_REG (PINE & 0x10)
  #define MOTOR_REG (PINE & 0x20)
#else
  #error "Invalid device configuration."
#endif

// Safety guarantees for adjustments to power
#if (E_BRAKE_POWER < 0 || E_BRAKE_POWER > 255)
  #error "Invalid value for E_BRAKE_POWER"
#elif (FAILSAFE_BRAKE_POWER < 0 || FAILSAFE_BRAKE_POWER > 255)
  #error "Invalid value for FAILSAFE_BRAKE_POWER"
#endif

// Interrupt variabbles
volatile unsigned long rx_servo_val;  // servo value
volatile unsigned long servo_count;     // temporary variable for servo PWM

volatile unsigned long rx_motor_val;  // servo value
volatile unsigned long motor_count;   // temporary variable for motor PWM

Servo servo;
Servo esc;
void setup() {
  Serial.begin(115200);

  servo.attach(SERVO_PIN);  // servo pin
  esc.attach(ESC_PIN);      // motor pin

  pinMode(RX_SERVO_PIN, INPUT);  // Rx servo pin
  pinMode(RX_MOTOR_PIN, INPUT);  // Rx motor pin
  pinMode(LED, OUTPUT);

  digitalWrite(LED, LOW);

  attachInterrupt(digitalPinToInterrupt(RX_SERVO_PIN), handleInterrupt_Servo, CHANGE);  // Catch up and down
  attachInterrupt(digitalPinToInterrupt(RX_MOTOR_PIN), handleInterrupt_Motor, CHANGE);  // Catch up and down
  

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  digitalWrite(LED, HIGH);
}

void loop() {
  static uint32_t last_update = 0;
  static bool failsafe = true;
  static bool armed = false;  // TODO: set to false once code is safe

  // State Errors (names taken from Betaflight warnings)
  static bool armSwitchSafe = false; // Armswitch must be off after boot to run commands
  static int32_t bootTime = millis(); // Will not arm for a couple of seconds
  
  // Arming logic
  if (!armed && armSwitchSafe && rx_motor_val >= 1800) {
    armed = true;
    Serial.flush();
    Serial.println("ARM");
  }

  // Arm at boot invalid logic
  else if (!armSwitchSafe && rx_motor_val != 0 && rx_motor_val < 1800) {
      armSwitchSafe = true;
  }

  // Armed logic
  else if (armed) {
    if (rx_motor_val <= 1200) {
      armed = false;
      failsafe = true;
      //servo.writeMicroseconds(convertToPulseLength(0));
      // Brakes at half speed
      esc.writeMicroseconds(convertToPulseLength(-E_BRAKE_POWER));
      Serial.println("DISARM");
    }
    
    // Serial processing and servo writing
    else if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      int delim_index = data.indexOf(',');

      // Input must have a comma in the middle somewhere
      if (delim_index > 0 && delim_index != data.length() - 1) {
        last_update = millis();

        int16_t motor_value = data.substring(0, delim_index).toInt();
        int16_t servo_value = data.substring(delim_index + 1, data.length()).toInt();
        servo.writeMicroseconds(convertToPulseLength(servo_value));
        esc.writeMicroseconds(convertToPulseLength(motor_value));
        failsafe = false;
      } 
      else {
        // Returns invalid input for debugging
        Serial.print("ERROR: ");
        Serial.println(data);
      }
    }
  }

  // No data detected in timespan, activating failsafe
  // TODO: Also check for loss of serial
  if (!failsafe && millis() >= last_update + TIMEOUT) {
    Serial.println("FAILSAFE");
    // Servo should keep its position and as such isn't changed
    esc.writeMicroseconds(convertToPulseLength(FAILSAFE_BRAKE_POWER));
    failsafe = true;
  }

  delay(5);
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
