
//define the two direction logic pins and the speed / PWM pin
const int DIR_A = 5;
const int DIR_B = 4;
const int PWM = 6;
const int calibratePower = 50;
const int calibrateTime = 25;
int calFlag = 1;

void setup()
{
Serial.begin(9600);
//set all pins as output
pinMode(DIR_A, OUTPUT);
pinMode(DIR_B, OUTPUT);
pinMode(PWM, OUTPUT);
//Off
digitalWrite(DIR_A, LOW);
digitalWrite(DIR_B, LOW);
analogWrite(PWM, 0);

while(1){
  if ((Serial.available() > 0) && (calFlag)) { // Check if data is available to read
    char command = Serial.read(); // Read the incoming command
    if (command == 'a') {
      //Counter-Clockwise
       digitalWrite(DIR_A, LOW);
       digitalWrite(DIR_B, HIGH);
       analogWrite(PWM, calibratePower);
       delay(calibrateTime);
       //Off
        digitalWrite(DIR_A, LOW);
        digitalWrite(DIR_B, LOW);
        analogWrite(PWM, 0);
    } else if (command == 'd') {
       //Clockwise
       digitalWrite(DIR_A, HIGH);
       digitalWrite(DIR_B, LOW);
       analogWrite(PWM, calibratePower);
       delay(calibrateTime);
       //Off
        digitalWrite(DIR_A, LOW);
        digitalWrite(DIR_B, LOW);
        analogWrite(PWM, 0);
    } else if(command == 'w'){
        break;
    }
}
}
while(1){
  if ((Serial.available() >= 3)) { // Check if data is available to read
    char data[3];
    for (int i = 0; i < 3; i++) {
      data[i] = Serial.read(); // Read the incoming characters
    }
    char direct = data[0];
    int sped = data[1] - '0';
    int tim = data[2] - '0';
    digitalWrite(DIR_A, HIGH);
       digitalWrite(DIR_B, LOW);
       analogWrite(PWM, calibratePower);
            if (direct == 'a') {
              //Counter-Clockwise
               digitalWrite(DIR_A, LOW);
               digitalWrite(DIR_B, HIGH);
               analogWrite(PWM, sped*25);
               delay(tim*250);
               //Off
                digitalWrite(DIR_A, LOW);
                digitalWrite(DIR_B, LOW);
                analogWrite(PWM, 0);
            } else if (direct == 'd') {
               //Clockwise
               digitalWrite(DIR_A, HIGH);
               digitalWrite(DIR_B, LOW);
               analogWrite(PWM, sped*25);
               delay(tim*250);
               //Off
                digitalWrite(DIR_A, LOW);
                digitalWrite(DIR_B, LOW);
                analogWrite(PWM, 0);
                  
              }
      }
}
}//end void setup

void loop()
{

}
