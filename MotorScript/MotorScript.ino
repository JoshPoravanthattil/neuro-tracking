
//define the two direction logic pins and the speed / PWM pin
const int DIR_A = 5;
const int DIR_B = 4;
const int PWM = 6;
const int calibratePower = 100;
const int calibrateTime = 100; // in ms
int calFlag = 1;

const int RED_PIN = 9;
const int GREEN_PIN = 10;

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
//LED
pinMode(RED_PIN, OUTPUT);
pinMode(GREEN_PIN, OUTPUT);
//make sure LEDs are off to begin
digitalWrite(RED_PIN, LOW);
digitalWrite(GREEN_PIN, LOW);

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
//turn red LED on
digitalWrite(RED_PIN, HIGH);
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
               analogWrite(PWM, sped*10);
               delay(tim*100);
               //Off
                digitalWrite(DIR_A, LOW);
                digitalWrite(DIR_B, LOW);
                analogWrite(PWM, 0);
            } else if (direct == 'd') {
               //Clockwise
               digitalWrite(DIR_A, HIGH);
               digitalWrite(DIR_B, LOW);
               analogWrite(PWM, sped*10);
               delay(tim*100);
               //Off
                digitalWrite(DIR_A, LOW);
                digitalWrite(DIR_B, LOW);
                analogWrite(PWM, 0);   
              }
              //activating LEDS requires this format 'gXX'
              //where Xs are burner inputs
              else if(direct == 'g'){
                //turn on green led
                digitalWrite(RED_PIN, LOW);
                digitalWrite(GREEN_PIN, HIGH);
                //Off
                digitalWrite(DIR_A, LOW);
                digitalWrite(DIR_B, LOW);
                analogWrite(PWM, 0); 
              }
              else if(direct == 'r'){
                //turn on red led
                digitalWrite(RED_PIN, HIGH);
                digitalWrite(GREEN_PIN, LOW);
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
