//bring in servo library
#include <Servo.h>
Servo myservo_top;
Servo myservo_bottom;
int servo_top = 6;
int servo_bottom = 5;
int light_pin = 12;

#include <IRremote.h>
int RECV_PIN = 13;

IRrecv irrecv(RECV_PIN);

decode_results results;


void setup() {
  // put your setup code here, to run once:

  //set up the light
  pinMode(light_pin, OUTPUT);

  // set up the servos to the desired configuration
  myservo_top.attach(servo_top, 1000, 2000);
  myservo_bottom.attach(servo_bottom, 500, 2000);

  //set the two servos to the starting position
  myservo_top.write(200);
  myservo_bottom.write(500);

  // code for the IR remote
  irrecv.enableIRIn();

  //begin serial monitor for debugging purposes
  Serial.begin(9600);
  

}

void loop() {
  // put your main code here, to run repeatedly:

  //code to test the button
  if (irrecv.decode(&results)){
    int value = results.value;
    int state = digitalRead(light_pin);
    Serial.println(value);
    
    if (value == 12495){                //corresponds to button 1 to turn on the light
      digitalWrite(light_pin, HIGH);
      myservo_top.write(550);
      delay(2000);
      digitalWrite(light_pin, LOW);
      myservo_top.write(200);
    }
    if (value == 6375){
      digitalWrite(light_pin, HIGH);
      myservo_bottom.write(800);
      delay(2000);
      digitalWrite(light_pin, LOW);
      myservo_bottom.write(500);
    }

    irrecv.resume();
  }
}