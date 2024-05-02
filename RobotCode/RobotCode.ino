#include <Arduino.h>

const int MAX_SIZE = 64; // The maximum size of the buffer
byte data[MAX_SIZE]; // Global buffer to hold received data
int data_length = 0; // Global variable to hold the length of the received data
int arrayLength = 0; // Global variable to track the length of the tokens and values arrays

// Global arrays for tokens and values
char tokens[32];
uint8_t values[32];

#define PIN_SONIC_TRIG      7 // Pin for sonar trigger
#define PIN_SONIC_ECHO      8 // Pin for sonar echo
#define MOTOR_DIRECTION     0 // If the direction is reversed, change 0 to 1
#define PIN_DIRECTION_LEFT  4
#define PIN_DIRECTION_RIGHT 3
#define PIN_MOTOR_PWM_LEFT  6
#define PIN_MOTOR_PWM_RIGHT 5

#define MAX_DISTANCE        1000 // Maximum distance for sonar measurement in cm
#define SONIC_TIMEOUT       (MAX_DISTANCE * 60) // Time out for sonar in microseconds
#define SOUND_VELOCITY      340 // Speed of sound in air (340 m/s)
#define SAFE_DISTANCE       40.0 // Define a safe distance threshold in cm

void setup() {
    Serial.begin(9600);
    pinMode(PIN_DIRECTION_LEFT, OUTPUT);
    pinMode(PIN_MOTOR_PWM_LEFT, OUTPUT);
    pinMode(PIN_DIRECTION_RIGHT, OUTPUT);
    pinMode(PIN_MOTOR_PWM_RIGHT, OUTPUT);
    pinMode(PIN_SONIC_TRIG, OUTPUT);
    pinMode(PIN_SONIC_ECHO, INPUT);
    
    // Set up the timer interrupt for sonar distance checks
    noInterrupts(); // Disable interrupts
    TCCR1A = 0; // Clear register A
    TCCR1B = 0; // Clear register B
    TCNT1 = 0; // Initialize counter
    OCR1A = 15624; // Set compare match value for 1 Hz interrupts (16MHz / 1024 / 1Hz)
    TCCR1B |= (1 << WGM12); // Configure timer 1 for CTC mode
    TCCR1B |= (1 << CS12) | (1 << CS10); // Set prescaler to 1024
    TIMSK1 |= (1 << OCIE1A); // Enable timer compare interrupt
    interrupts(); // Enable interrupts
}

// Timer 1 ISR for sonar distance checks
ISR(TIMER1_COMPA_vect) {
    float distance = getSonarDistance();
    
    // Declare a static flag to track if the message has been printed
    static bool messagePrinted = false;
    
    // Check if distance is less than safe distance
    if (distance < SAFE_DISTANCE) {
        // Check if the message has not been printed yet
        if (!messagePrinted) {
            // Print the message once and set the flag to true
            Serial.println("Obstacle detected! Stopping the vehicle.");
            messagePrinted = true;
        }
        // Stop the vehicle
        motorRun(0, 0);
    } else {
        // Reset the flag if the distance is above safe distance
        messagePrinted = false;
    }
}

// Function to measure sonar distance
float getSonarDistance() {
    digitalWrite(PIN_SONIC_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_SONIC_TRIG, LOW);
    
    unsigned long pingTime = pulseIn(PIN_SONIC_ECHO, HIGH, SONIC_TIMEOUT);
    float distance = 0;
    if (pingTime != 0) {
        distance = (float)pingTime * SOUND_VELOCITY / 2 / 10000;
    } else {
        distance = MAX_DISTANCE;
    }
    
    return distance;
}

// Call execute_actions in loop function
void loop() {
    if (Serial.available()) {
        resetValues();
        download_data();
        if (checksum()) {
            Serial.println("Received data, Running Program");
            unpack_data();
            execute_actions();
            Serial.println("End of Program");
        }
    }
}

void resetValues() {
    // Reset the global variables to their initial states
    memset(data, 0, sizeof(data)); // Reset the data buffer to all zeros
    data_length = 0; // Reset the data length to zero
    arrayLength = 0; // Reset the array length to zero

    // Reset the tokens and values arrays to all zeros
    memset(tokens, 0, sizeof(tokens));
    memset(values, 0, sizeof(values));
}

void download_data() {
    // Read data from serial communication into the buffer
    while (Serial.available() && data_length < MAX_SIZE) {
        // Read one byte at a time from serial and store it in the buffer
        data[data_length] = Serial.read();
        // Increment the length of the received data
        data_length++;
        // Short delay to allow time for more data to arrive
        delay(10);
    }
}

bool checksum() {
    // Extract checksum from the last byte of the data
    byte receivedChecksum = data[data_length - 1];

    // Calculate checksum of received data (excluding the last byte)
    byte calculatedChecksum = 0;
    for (int i = 0; i < data_length - 1; i++) {
        calculatedChecksum += data[i];
    }

    // Compare calculated checksum with received checksum
    if (calculatedChecksum != receivedChecksum) {
        Serial.println("Checksum mismatch: Data may be corrupted.");
        return false; // Return false if there is a checksum mismatch
    }

    // Return true if checksums match
    return true;
}

void unpack_data() {
    // Use the global variables data and data_length
        int index = 0;
        arrayLength = 0; // Reset the arrayLength to 0

    while (index < data_length - 1) {
        // Read the token
        char token = data[index];
        index++;

        // Read the value
        uint8_t value = data[index];
        index++;

        // Store the token and value in arrays
        tokens[arrayLength] = token;
        values[arrayLength] = value;

        // Increment the array length
        arrayLength++;
    }
}

void execute_actions() {
    for (int i = 0; i < arrayLength; i++) {
        char token = tokens[i];
        uint8_t value = values[i];
        
        if (token == 'f') {
            // Handle the for loop loop
            uint8_t loop_count = value; // Number of times to repeat
            i++; // Move to the next token after 'f'
            
            // Store the start of the loop block
            int loop_start = i;
            
            // Find the end of the loop block marked by token 'e'
            int loop_end = -1;
            for (int j = i; j < arrayLength; j++) {
                if (tokens[j] == 'e') {
                    loop_end = j;
                    break;
                }
            }
            
            // If 'e' is found
            if (loop_end != -1) {
                // Execute the loop block loop_count times
                for (int k = 0; k < loop_count; k++) {
                    for (int j = loop_start; j < loop_end; j++) {
                        execute_single_action(tokens[j], values[j]);
                    }
                }
                
                // Move the index to the end of the loop block
                i = loop_end;
            } else {
                // If 'e' token not found, print an error message
                Serial.println("Error: Unable to find end token for for loop.");
            }
        } else {
            // Handle individual action
            execute_single_action(token, value);
        }
    }
}

// Function to handle individual actions
void execute_single_action(char token, uint8_t value) {
    switch (token) {
        case 'M': // MOV
            move(value);
            break;
        case 'L': // TURNL
            turnLeft(value);
            break;
        case 'R': // TURNR
            turnRight(value);
            break;
        case 'S': // STOP
            stop(value);
            break;
        default:
            Serial.print("Unknown token: ");
            Serial.println(token);
            break;
    }
}


// Placeholder functions for execution
void move(int steps) {
    if(steps < 0) {
      Serial.print("Moving back ");
      Serial.print(steps);
      Serial.println(" steps.");
      motorRun(-200, -200);
      delay(steps * 1000); 
      motorRun(0, 0);
    }

    if(steps > 0) {
      Serial.print("Moving forward ");
      Serial.print(steps);
      Serial.println(" steps.");
      motorRun(200, 200);
      delay(steps * 1000); 
      motorRun(0, 0);
    }
}

void turnLeft(int degrees) {
    Serial.print("Turning left ");
    Serial.print(degrees);
    Serial.println(" degrees.");

    // Determine the turning rate (degrees per second)
    float turningRate = 90;

    // Calculate the time needed to turn the specified degrees
    float timeToTurn = degrees / turningRate;

    // Control the motors to turn left
    // Set the right motor forward and the left motor backward
    motorRun(-200, 200);

    // Delay for the calculated time
    delay(timeToTurn * 1000); // Convert time to milliseconds

    // Stop the motors
    motorRun(0, 0);
}

void turnRight(int degrees) {
    Serial.print("Turning right ");
    Serial.print(degrees);
    Serial.println(" degrees.");

    // Determine the turning rate (degrees per second)
    float turningRate = 90;

    // Calculate the time needed to turn the specified degrees
    float timeToTurn = degrees / turningRate;

    // Control the motors to turn right
    // Set the left motor forward and the right motor backward
    motorRun(200, -200);

    // Delay for the calculated time
    delay(timeToTurn * 1000); // Convert time to milliseconds

    // Stop the motors
    motorRun(0, 0);
}


void stop(int seconds) {
    Serial.print("Stopping ");
    Serial.print(seconds);
    Serial.println(" Secounds");
    motorRun(0, 0);
    delay(seconds * 1000); // Times 1000 so the seconds value corrisponds to the delay function (1000 = 1 second)
}

void motorRun(int speedl, int speedr) {
  int dirL = 0, dirR = 0;
  if (speedl > 0) {
    dirL = 0 ^ MOTOR_DIRECTION;
  } else {
    dirL = 1 ^ MOTOR_DIRECTION;
    speedl = -speedl;
  }

  if (speedr > 0) {
    dirR = 1 ^ MOTOR_DIRECTION;
  } else {
    dirR = 0 ^ MOTOR_DIRECTION;
    speedr = -speedr;
  }
  digitalWrite(PIN_DIRECTION_LEFT, dirL);
  digitalWrite(PIN_DIRECTION_RIGHT, dirR);
  analogWrite(PIN_MOTOR_PWM_LEFT, speedl);
  analogWrite(PIN_MOTOR_PWM_RIGHT, speedr);
}

