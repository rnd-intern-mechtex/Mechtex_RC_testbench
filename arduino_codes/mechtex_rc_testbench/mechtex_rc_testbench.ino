#include <SoftwareSerial.h>
#include <Servo.h>

#define PWM_PIN 9
#define LOADCELL_BUFFER 8

Servo esc;
SoftwareSerial LoadCell(10, 11);

uint16_t numSamples = 100;
uint16_t currentPwm = 1000;
float currentThrust = 0;
uint32_t currentRPM = 0;
uint8_t count = 0;
bool msgReady = false;
char message[50];
char loadcell_buf[LOADCELL_BUFFER];

void setup() {

  Serial.begin(9600);
  LoadCell.begin(2400);

  esc.attach(9, 1000, 2000);

  while (Serial.available()) {
    Serial.read();
  }
  Serial.flush();

  esc.write(map(currentPwm, 1000, 2000, 0, 180));

}

void loop() {

  if (msgReady) {
    decode_message();
    msgReady = false;
  }
  else while (Serial.available()) {
      char c = Serial.read();
      message[count++] = c;
      if (c == '\n') {
        message[count] = '\0';
        count = 0;
        msgReady = true;
      }
    }

  currentThrust = 321.00;
  currentRPM = 9870.0;

  

}


/*__________FUNCTIONS________________________________________________*/

void decode_message() {
  switch (message[0]) {
    case 'A':
      numSamples = atoi(&message[1]);
      break;
    case 'P':
      setPwm(atoi(&message[1]));
      break;
    case 'T':
      // return thrust
      Serial.print("T" + String(currentThrust) + "\n");
    case 'R':
      // return rpm
      Serial.print("R" + String(currentRPM) + "\n");
    case 'X':
      // return pwm
      Serial.print("P" + String(currentPwm) + "\n");
  }
}

float getThrust() {
  while (LoadCell.read() != 0x5B);
  LoadCell.readBytes(loadcell_buf, LOADCELL_BUFFER);
  if (loadcell_buf[LOADCELL_BUFFER - 1] == 0x40) {
    return 0;
  }
  if (loadcell_buf[LOADCELL_BUFFER] == 0x0B) {
    return convertToFloat(loadcell_buf);
  }
  getThrust();
}

void getAvgThrust() {
  float sum = 0;
  for (uint8_t i = 0; i < numSamples; i++) {
    sum += getThrust();
    delay(50);
  }
  currentThrust = sum / numSamples;
}

void setPwm(uint16_t value) {

  if ((value < 1000) || (value > 2000)) {
#ifdef DEBUG
    Serial.println("Invalid PWM Period ...");
    Serial.println("Enter value from 1000 to 2000 (ms) ...");
#endif
    return;
  }
  if (value == currentPwm) {
#ifdef DEBUG
    Serial.println("Requested Pwm Value same as current Pwm Value ...");
#endif
    return;
  }
  esc.write(map(value, 1000, 2000, 0, 180));
  currentPwm = value;
}

float getRPM() {

}

void getAvgRPM() {

}

/*__________HELPER FUNCTIONS_________________________________________*/

float convertToFloat(char*) {
  /*
    This functions takes a character array of length 7
    Returns a float number with 3 decimal places
    Example:
    Input Char Array ['0', '0', '0', '5', '9', '9', '3', 0x03]
    Function Returns 5.993
  */

  char fractionPart[4];
  char integerPart[5];

  for (uint8_t i = 0; i < 3; i++) {
    fractionPart[i] = loadcell_buf[i + 4];
  }
  for (uint8_t i = 0; i < 4; i++) {
    integerPart[i] = loadcell_buf[i];
  }

  fractionPart[3] = '\0';
  integerPart[4] = '\0';

  float fraction = atof(fractionPart) / 1000.0;
  float finalValue = atof(integerPart) + fraction;

  return finalValue;
}
