#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

// MPU6050 and LCD configurations
Adafruit_MPU6050 mpu;
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Define servo objects
Servo servo1, servo2, servo3, servo4;

// Thresholds for servo control
const int ACCEL_THRESHOLD_X = 10;
const int ACCEL_THRESHOLD_Y = 10;
const int SERVO_NEUTRAL = 90;  // Middle position for servos
const int SERVO_MIN = 0;       // Minimum position for servos
const int SERVO_MAX = 180;     // Maximum position for servos

// Function Prototypes
void initializeMPU();
void initializeLCD();
void initializeServos();
void updateServoPositions(float accelX, float accelY);
void displayGyroData(sensors_event_t& g);
void handleServoMovement(int x, int y);

void setup() {
  Serial.begin(115200);

  initializeLCD();
  initializeMPU();
  initializeServos();
}

void loop() {
  // Get new sensor events with the readings
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Update LCD with gyro data
  displayGyroData(g);

  // Update servo positions based on accelerometer values
  handleServoMovement(a.acceleration.x, a.acceleration.y);

  // Delay for stabilization (optional)
  delay(100);
}

// Initialize MPU-6050 sensor
void initializeMPU() {
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  // Set accelerometer range to +-8G
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  // Set gyro range to +- 500 deg/s
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  // Set filter bandwidth to 184 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_184_HZ);

  delay(100);
  Serial.println("MPU6050 initialized");
}

// Initialize LCD display
void initializeLCD() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(1000);
}

// Initialize servos and set to neutral position
void initializeServos() {
  servo1.attach(7);
  servo2.attach(6);
  servo3.attach(5);
  servo4.attach(4);

  // Set all servos to the neutral position
  servo1.write(SERVO_NEUTRAL);
  servo2.write(SERVO_NEUTRAL);
  servo3.write(SERVO_NEUTRAL);
  servo4.write(SERVO_NEUTRAL);
  Serial.println("Servos initialized");
}

// Display gyro data on the LCD
void displayGyroData(sensors_event_t& g) {
  lcd.setCursor(0, 0);
  lcd.print("Roll: ");
  lcd.print(g.gyro.x, 2); // Display with 2 decimal places

  lcd.setCursor(0, 1);
  lcd.print("Pitch: ");
  lcd.print(g.gyro.y, 2); // Display with 2 decimal places
}

// Handle servo movement based on accelerometer readings
void handleServoMovement(float accelX, float accelY) {
  // Convert accelerometer values to integer format for comparison
  int x = (int)accelX;
  int y = (int)accelY;

  // Print acceleration data to the serial monitor for debugging
  Serial.print("X: ");
  Serial.print(x);
  Serial.print(" Y: ");
  Serial.println(y);

  // Servo movement conditions for X-axis (forward/backward movement)
  if (x > 0 && x <= ACCEL_THRESHOLD_X && abs(y) < 4) {
    Serial.println("Moving Up");
    int value1 = map(x, 0, ACCEL_THRESHOLD_X, SERVO_NEUTRAL, SERVO_MAX);
    int value2 = map(x, 0, ACCEL_THRESHOLD_X, SERVO_NEUTRAL, SERVO_MIN);
    servo1.write(value1);
    servo2.write(value2);
  } else if (x < 0 && x >= -ACCEL_THRESHOLD_X && abs(y) < 4) {
    Serial.println("Moving Down");
    int value1 = map(x, -ACCEL_THRESHOLD_X, 0, SERVO_MIN, SERVO_NEUTRAL);
    int value2 = map(x, -ACCEL_THRESHOLD_X, 0, SERVO_MAX, SERVO_NEUTRAL);
    servo1.write(value1);
    servo2.write(value2);
  }

  // Servo movement conditions for Y-axis (left/right movement)
  if (y > 0 && y <= ACCEL_THRESHOLD_Y && abs(x) < 4) {
    Serial.println("Moving Right");
    int value3 = map(y, 0, ACCEL_THRESHOLD_Y, SERVO_NEUTRAL, SERVO_MAX);
    int value4 = map(y, 0, ACCEL_THRESHOLD_Y, SERVO_NEUTRAL, SERVO_MIN);
    servo3.write(value3);
    servo4.write(value4);
  } else if (y < 0 && y >= -ACCEL_THRESHOLD_Y && abs(x) < 4) {
    Serial.println("Moving Left");
    int value3 = map(y, -ACCEL_THRESHOLD_Y, 0, SERVO_MIN, SERVO_NEUTRAL);
    int value4 = map(y, -ACCEL_THRESHOLD_Y, 0, SERVO_MAX, SERVO_NEUTRAL);
    servo3.write(value3);
    servo4.write(value4);
  }
}
