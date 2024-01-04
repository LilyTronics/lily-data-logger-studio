/*
 * Firmware for turing the Arduino into a data logger.
 * Serial commands:
 *   rdx    : read digital input (x = 2 - 13)
 *   wdx 0/1: write 0/1 to digital output (x = 2 - 13)
 *   rax    : read analog input (x = 0 - 5)
 */

String rx_data;

void setup() {
    // Define all as inputs (save)
    for (int i = 2; i < 14; i++) {
        pinMode(i, INPUT);
    }
    Serial.begin(115200);
}

void loop() {
    if (Serial.available() > 0) {
        rx_data = Serial.readStringUntil('\n');
        if (rx_data.startsWith("rd")) {
            // Read digital
            int channel = rx_data.substring(2).toInt();
            if (channel > 1 && channel < 14) {
                pinMode(channel, INPUT);
                Serial.print(digitalRead(channel));
                Serial.print('\n');
            }
        }
        else if (rx_data.startsWith("wd")) {
            // Write digital
            int space_index = rx_data.indexOf(' ');
            if (space_index > 2) {
                int channel = rx_data.substring(2, space_index).toInt();
                if (channel > 1 && channel < 14) {
                    int value = rx_data.substring(space_index).toInt();
                    if (value > -1 && value < 2) {
                        pinMode(channel, OUTPUT);
                        digitalWrite(channel, value);
                    }
                }
            }
        }
        else if (rx_data.startsWith("ra")) {
            // Read analog
            int channel = rx_data.substring(2).toInt();
            if (channel > -1 && channel < 6) {
                int adc = analogRead(channel + A0);
                Serial.print(adc * 5.0 / 1023, 3);
                Serial.print('\n');
            }
        }
    }
}
