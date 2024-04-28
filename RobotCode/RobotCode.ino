#include <Arduino.h>

const int MAX_SIZE = 64; // The maximum size of the buffer
byte data[MAX_SIZE]; // Global buffer to hold received data
int data_length = 0; // Global variable to hold the length of the received data
int arrayLength = 0; // Global variable to track the length of the tokens and values arrays

// Global arrays for tokens and values
char tokens[32];
uint8_t values[32];

void setup() {
    Serial.begin(9600);
}

// Call execute_actions in loop function
void loop() {
    if (Serial.available()) {
        resetValues();
        download_data();
        if (checksum()) {
            Serial.println("Received data");
            unpack_data();
            execute_actions();
            Serial.println("End of received data");
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
    // Implement move functionality
    Serial.print("Moving ");
    Serial.print(steps);
    Serial.println(" steps.");
}

void turnLeft(int degrees) {
    // Implement turn left functionality
    Serial.print("Turning left ");
    Serial.print(degrees);
    Serial.println(" degrees.");
}

void turnRight(int degrees) {
    // Implement turn right functionality
    Serial.print("Turning right ");
    Serial.print(degrees);
    Serial.println(" degrees.");
}

void stop(int seconds) {
    // Implement stop functionality
    Serial.print("Stopping.");
    Serial.print(seconds);
    Serial.println(" Secounds");
}

