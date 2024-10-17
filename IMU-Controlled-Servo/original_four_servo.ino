#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

Adafruit_MPU6050 mpu;
LiquidCrystal_I2C lcd(0x27, 16, 2);

int x = 0;
int y = 0;
int z = 0;

Servo servo1; 
Servo servo2;
Servo servo3;
Servo servo4;

int value  = 0;

void setup(void) {
  Serial.begin(115200);

  lcd.begin();
  lcd.backlight();
  mpu.begin();

  // set accelerometer range to +-8G
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  // set gyro range to +- 500 deg/s
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  // set filter bandwidth to 21 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_184_HZ);

  delay(100);
  servo1.attach(7);
  servo2.attach(6); 
  servo3.attach(5); 
  servo4.attach(4); 

  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  x = a.acceleration.x;
  y = a.acceleration.y;
  z = a.acceleration.z;

  lcd.setCursor(0, 0);
  lcd.print("Roll:");
  lcd.print(g.gyro.x);

  lcd.setCursor(0, 1);
  lcd.print("Pitch:");
  lcd.print(g.gyro.y);

//  lcd.setCursor(8, 0);
//  lcd.print("Yaw:");
//  lcd.print(g.gyro.z);
  //delay(100);
Serial.print(x);Serial.print(" ");Serial.println(y); 
if (x < 10 && x > 0 && y < 4 && y > -4){    //זה טוב
  Serial.println("up");
   int value1 = map(x,  0, 10, 90, 180);
   servo1.write(value1);
   int value2 = map(x,  0, 10, 90, 0);
   servo2.write(value2);
   
   Serial.print(value);
  }
else if (x > -10 && x < 0 && y < 4 && y > -4){
  Serial.println("down");
  int value3 = map(x,  -10, 0,0, 90);
  servo1.write(value3);
  int value4 = map(x,  -10, 0, 180, 90);
  servo2.write(value4);
  Serial.print(value);
  }

if (y < 10 && y > 0 && x < 4 && x > -4){ //זה טוב 
  Serial.println("Right");
  int value5 = map(y,  0, 10, 90, 180);
  servo3.write(value5);
  int value6 = map(y,  0, 10, 90, 0);
  servo4.write(value6);
  Serial.print(value);
  }
else if (y > -10 && y < 0  && x < 4 && x > -4){
  Serial.println("left");
  int value7 = map(y,  -10, 0, 0, 90);
  servo3.write(value7);
  int value8 = map(y,  -10, 0, 180, 90);
  servo4.write(value8);
  Serial.print(value);
  }
}
