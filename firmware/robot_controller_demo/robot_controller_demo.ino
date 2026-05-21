// Sanitized Arduino Mega 2560 demo skeleton.
// This file demonstrates finite-state-machine organization only.
// It is not a complete hardware-tuned firmware release.

enum RobotState {
  LEAVE_BAY,
  LINE_FOLLOW_TO_PICK,
  TARGET_CONFIRM,
  PICK_OBJECT,
  COLOR_CLASSIFY,
  SORT_DROP,
  RETURN_HOME,
  COMPLETE
};

RobotState state = LEAVE_BAY;
unsigned long stateStartMs = 0;

void enterState(RobotState nextState) {
  state = nextState;
  stateStartMs = millis();
  Serial.print("enter_state=");
  Serial.println((int)state);
}

int readLineErrorDemo() {
  return analogRead(A0) - 512;
}

float readDistanceCmDemo() {
  return 22.0;  // Placeholder for HC-SR04 integration in the real build.
}

void setDrivePwm(int leftPwm, int rightPwm) {
  Serial.print("left_pwm=");
  Serial.print(leftPwm);
  Serial.print(",right_pwm=");
  Serial.println(rightPwm);
}

void lineFollowStep() {
  int error = readLineErrorDemo();
  int correction = constrain(error / 8, -45, 45);
  setDrivePwm(145 - correction, 145 + correction);
}

void setup() {
  Serial.begin(115200);
  enterState(LEAVE_BAY);
}

void loop() {
  unsigned long elapsed = millis() - stateStartMs;
  switch (state) {
    case LEAVE_BAY:
      setDrivePwm(135, 135);
      if (elapsed > 1500) enterState(LINE_FOLLOW_TO_PICK);
      break;
    case LINE_FOLLOW_TO_PICK:
      lineFollowStep();
      if (elapsed > 5000) enterState(TARGET_CONFIRM);
      break;
    case TARGET_CONFIRM:
      setDrivePwm(0, 0);
      if (readDistanceCmDemo() < 30.0 || elapsed > 1200) enterState(PICK_OBJECT);
      break;
    case PICK_OBJECT:
      if (elapsed > 1600) enterState(COLOR_CLASSIFY);
      break;
    case COLOR_CLASSIFY:
      if (elapsed > 1000) enterState(SORT_DROP);
      break;
    case SORT_DROP:
      if (elapsed > 1800) enterState(RETURN_HOME);
      break;
    case RETURN_HOME:
      lineFollowStep();
      if (elapsed > 5000) enterState(COMPLETE);
      break;
    case COMPLETE:
      setDrivePwm(0, 0);
      break;
  }
}

