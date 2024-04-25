#include <Arduino.h>
const int MAX_SIZE = 64; // Define the maximum size of the buffer
byte data[MAX_SIZE]; // Global buffer to hold received data
int data_length = 0; // Global variable to hold the length of the received data

void setup() {
  Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        download_data();
        // Only call unpack_data if data_length > 0
        if (data_length > 0) {
            unpack_data(); // Call unpack_data without parameters
        }
    }
}

void download_data() {
    // Reset the global variables to their initial states
    memset(data, 0, sizeof(data)); // Reset the data buffer to all zeros
    data_length = 0; // Reset the data length to zero

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
    if (checksum()) {
        int index = 0;
        while (index < data_length - 1) {
            char token = data[index];
            index++;
            uint8_t value = data[index];
            index++;
            Serial.print("Token: ");
            Serial.print(token);
            Serial.print(", Value: ");
            Serial.println(value);
        }
    }
}




