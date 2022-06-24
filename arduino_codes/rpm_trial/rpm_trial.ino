
#include <Servo.h>
#define PWM_PIN 9
Servo esc;

uint16_t currentPwm = 1000;
bool msgReady = false;
char message[50];
uint8_t count = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  esc.attach(9, 1000, 2000);
  pinMode(8, INPUT_PULLUP);

  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= 0b10000101;
  TIMSK1 |= 0b00100000;
  TCNT1 = 0;
  interrupts();

  while (Serial.available()) {
    Serial.read();
  }
  Serial.flush();

  esc.write(map(currentPwm, 1000, 2000, 0, 180));

}

ISR(TIMER1_CAPT_vect) {
  int input_capture = ICR1;
  Serial.println("HELLO");
}

void loop() {
  // put your main code here, to run repeatedly:
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

}

void decode_message() {
  switch (message[0]) {
    case 'P':
      setPwm(atoi(&message[1]));
      break;
    case 'R':
      // return rpm
      break;
  }
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
