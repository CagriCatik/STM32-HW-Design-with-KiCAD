

### 1. **Libraries and Objects Initialization**:

```cpp
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>
```
- **Adafruit_MPU6050**, **Adafruit_Sensor**, **Wire**: These libraries manage communication and interaction with the MPU6050 sensor via I2C, as well as accessing the sensor’s accelerometer and gyroscope data.
- **Servo.h**: This is used to control the servos.
- **LiquidCrystal_I2C.h**: Handles communication with an I2C-based LCD display for real-time information output.

#### Objects:

```cpp
Adafruit_MPU6050 mpu;
LiquidCrystal_I2C lcd(0x27, 16, 2);
```
- **mpu**: An object to interface with the MPU6050 accelerometer and gyroscope.
- **lcd**: Object to interface with the I2C LCD (address `0x27`), which is 16 columns and 2 rows in size.

---

### 2. **Servo Configuration**:

```cpp
Servo servo1, servo2, servo3, servo4;
```
- These four servo objects control the servos attached to the Arduino.

---

### 3. **Constants and Thresholds**:

```cpp
const int ACCEL_THRESHOLD_X = 10;
const int ACCEL_THRESHOLD_Y = 10;
const int SERVO_NEUTRAL = 90;
const int SERVO_MIN = 0;
const int SERVO_MAX = 180;
```
- **ACCEL_THRESHOLD_X** and **ACCEL_THRESHOLD_Y**: Define the thresholds for accelerometer values in the X and Y axes, determining when and how much the servos will move.
- **SERVO_NEUTRAL**: The neutral or centered position for each servo, which corresponds to 90°.
- **SERVO_MIN** and **SERVO_MAX**: Define the minimum (0°) and maximum (180°) positions for the servos. These values map the accelerometer readings to the servos' physical range of movement.

---

### 4. **Function Prototypes**:

```cpp
void initializeMPU();
void initializeLCD();
void initializeServos();
void updateServoPositions(float accelX, float accelY);
void displayGyroData(sensors_event_t& g);
void handleServoMovement(int x, int y);
```
These are the function prototypes, declaring the functions that are used later in the code for initialization, updating servos, and displaying sensor data.

---

### 5. **Setup Function**:

```cpp
void setup() {
  Serial.begin(115200);

  initializeLCD();
  initializeMPU();
  initializeServos();
}
```
- **Serial.begin(115200)**: Starts serial communication at a baud rate of 115200 for debugging and displaying output in the Serial Monitor.
- **initializeLCD()**, **initializeMPU()**, **initializeServos()**: These functions handle the initialization of the LCD, MPU6050 sensor, and servos. Breaking down initialization into separate functions improves code organization and clarity.

---

### 6. **Main Loop**:

```cpp
void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  displayGyroData(g);

  handleServoMovement(a.acceleration.x, a.acceleration.y);

  delay(100);
}
```
- The **loop()** function continuously runs, reading sensor data, updating the LCD with the current gyroscope values, and controlling servo movements based on accelerometer readings.

1. **sensors_event_t a, g, temp**: These hold the sensor data returned from the MPU6050: `a` for accelerometer, `g` for gyroscope, and `temp` for temperature.
   
2. **mpu.getEvent(&a, &g, &temp)**: Retrieves the current sensor readings from the MPU6050. This fills the accelerometer, gyroscope, and temperature data structures.

3. **displayGyroData(g)**: Updates the LCD with the current gyroscope values for roll and pitch.

4. **handleServoMovement(a.acceleration.x, a.acceleration.y)**: Uses the accelerometer's X and Y axis values to determine how the servos should move, adjusting based on thresholds.

5. **delay(100)**: A short delay to stabilize servo movement and prevent excessive updates.

---

### 7. **Initializing MPU-6050**:

```cpp
void initializeMPU() {
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_184_HZ);

  delay(100);
  Serial.println("MPU6050 initialized");
}
```
- This function sets up the MPU6050:
  - **mpu.begin()**: Initializes communication with the sensor. If it fails, the system halts.
  - **mpu.setAccelerometerRange(MPU6050_RANGE_8_G)**: Configures the accelerometer range to ±8g.
  - **mpu.setGyroRange(MPU6050_RANGE_500_DEG)**: Configures the gyroscope range to ±500°/sec.
  - **mpu.setFilterBandwidth(MPU6050_BAND_184_HZ)**: Sets a filter bandwidth to reduce noise in the sensor data.
  - **Serial.println("MPU6050 initialized")**: Confirms successful initialization via the Serial Monitor.

---

### 8. **Initializing the LCD**:

```cpp
void initializeLCD() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(1000);
}
```
- Initializes the LCD and prints "Initializing..." as feedback during startup. The LCD is cleared after initialization.

---

### 9. **Initializing the Servos**:

```cpp
void initializeServos() {
  servo1.attach(7);
  servo2.attach(6);
  servo3.attach(5);
  servo4.attach(4);

  servo1.write(SERVO_NEUTRAL);
  servo2.write(SERVO_NEUTRAL);
  servo3.write(SERVO_NEUTRAL);
  servo4.write(SERVO_NEUTRAL);
  Serial.println("Servos initialized");
}
```
- **servoX.attach()**: Attaches each servo to its respective pin on the Arduino.
- **servoX.write(SERVO_NEUTRAL)**: Sets each servo to its neutral (90°) position at startup.

---

### 10. **Displaying Gyro Data on the LCD**:

```cpp
void displayGyroData(sensors_event_t& g) {
  lcd.setCursor(0, 0);
  lcd.print("Roll: ");
  lcd.print(g.gyro.x, 2);  // Displays roll with 2 decimal places

  lcd.setCursor(0, 1);
  lcd.print("Pitch: ");
  lcd.print(g.gyro.y, 2);  // Displays pitch with 2 decimal places
}
```
- This function displays the current **roll** and **pitch** values (from the gyroscope) on the LCD.

---

### 11. **Handling Servo Movements**:

```cpp
void handleServoMovement(float accelX, float accelY) {
  int x = (int)accelX;
  int y = (int)accelY;

  Serial.print("X: ");
  Serial.print(x);
  Serial.print(" Y: ");
  Serial.println(y);

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

  if (y > 0 && y <= ACCEL_THRESHOLD_Y && abs(x) < 4) {
    Serial.println("Moving Right");
    int value3 = map(y, 0, ACCEL_THRESHOLD_Y, SERVO_NEUTRAL, SERVO_MAX);
    int value4 = map(y, 0, ACCEL_THRESHOLD_Y, SERVO_NEUTRAL, SERVO_MIN);
    servo3.write(value3);
    servo4.write(value4);
  } else if (y < 0 && y >= -ACCEL_THRESHOLD_Y && abs(x) < 4) {
    Serial.println("Moving Left");
    int value3 = map(y, -ACCEL_THRESHOLD_Y, 0, SERVO_MIN,

 SERVO_NEUTRAL);
    int value4 = map(y, -ACCEL_THRESHOLD_Y, 0, SERVO_MAX, SERVO_NEUTRAL);
    servo3.write(value3);
    servo4.write(value4);
  }
}
```
- **handleServoMovement()**: This function reads the X and Y accelerometer values and maps them to the servo positions:
  - For the **X-axis**, if the value is between `-10` and `10`, it controls `servo1` and `servo2`, simulating forward/backward movement.
  - For the **Y-axis**, it controls `servo3` and `servo4`, simulating left/right movement.
  - **map()**: Maps accelerometer readings to the servos' angle range (0° to 180°).

---

### Conclusion:
- The code uses an MPU6050 sensor to read real-time accelerometer and gyroscope data, which is displayed on an LCD and used to control four servos. The servos are adjusted based on the tilt or orientation (pitch and roll) detected by the accelerometer, making this a robust system for controlling servos based on motion.
- This modular design makes it easy to read, extend, and maintain.


The last code controls **four servos**. Here's a breakdown of their purposes:

### 1. **Servo1 and Servo2**:
- **Purpose**: These two servos are responsible for handling movements along the **X-axis**, which represents forward and backward tilt or motion based on the accelerometer's X-axis readings.
- **How they work**: 
  - If the tilt in the X direction is positive (forward), **Servo1** moves from its neutral position (90°) toward the maximum position (180°), while **Servo2** moves in the opposite direction (toward 0°).
  - If the tilt in the X direction is negative (backward), **Servo1** moves from its neutral position (90°) toward the minimum position (0°), while **Servo2** moves toward the maximum position (180°).
  
This configuration creates a counteracting motion between the two servos, simulating a forward/backward movement.

### 2. **Servo3 and Servo4**:
- **Purpose**: These two servos are responsible for handling movements along the **Y-axis**, which represents left and right tilt or motion based on the accelerometer's Y-axis readings.
- **How they work**: 
  - If the tilt in the Y direction is positive (rightward), **Servo3** moves from its neutral position (90°) toward the maximum position (180°), while **Servo4** moves toward the minimum position (0°).
  - If the tilt in the Y direction is negative (leftward), **Servo3** moves from its neutral position (90°) toward the minimum position (0°), while **Servo4** moves toward the maximum position (180°).

This setup simulates left and right motion, creating counteracting movements for balance.

---

### **Summary of Servos' Purposes**:
- **Servo1 and Servo2**: Control forward and backward tilt based on the X-axis accelerometer readings.
- **Servo3 and Servo4**: Control left and right tilt based on the Y-axis accelerometer readings.

Together, the four servos allow for a controlled response to tilting motion along both axes, potentially for applications like balancing mechanisms, stabilization systems, or directional control of a vehicle or object based on real-time sensor feedback.