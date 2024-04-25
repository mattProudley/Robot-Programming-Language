#include <Arduino.h>
const int MAX_SIZE = 64;  // Define the maximum size of the buffer

void setup() {
  Serial.begin(9600);
}

void loop() {
      if(Serial.available()) {
        download_data();
    }
}


void download_data() {

    // Define buffer to hold the received data
    byte receivedData[MAX_SIZE];

    // Variable to track the length of the received data
    int receivedLength = 0;

    // Read data from serial communication into the buffer
    while (Serial.available() && receivedLength < MAX_SIZE) {
        // Read one byte at a time from serial and store it in the buffer
        receivedData[receivedLength] = Serial.read();
        // Increment the length of the received data
        receivedLength++;
        // Short delay to allow time for more data to arrive
        delay(10);
    }

    unpack_data(receivedData, receivedLength);
}

  void unpack_data(byte receivedData[], int receivedLength) {
    // Variables to hold the current index and token
    int index = 0;

    // Iterate over the received data
    while (index < receivedLength) {
        // Unpack token (1 byte) as a character
        char token = receivedData[index];
        index++;  // Move to the next byte

        // Unpack value (1 byte) as an unsigned 8-bit integer
        uint8_t value = receivedData[index];
        index++;  // Move to the next byte

        // Print the unpacked token and value
        Serial.print("Token: ");
        Serial.print(token);
        Serial.print(", Value: ");
        Serial.println(value);

        // You can process the token and value here as needed
        // For example, store them in a data structure, perform some calculations, etc.
    }
}


