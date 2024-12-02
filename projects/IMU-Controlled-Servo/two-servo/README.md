# Servo Controlling based on accelerometer data from MPU6050


1. **ServoX**: This servo is connected to pin 8 and is responsible for controlling the roll.
2. **ServoY**: This servo is connected to pin 9 and is responsible for controlling the pitch.

## 1. **Libraries and Definitions**:
```cpp
#include <SPI.h>
#include <Wire.h>
#include <Servo.h>
#include <math.h>
```
- **SPI.h** and **Wire.h**: These libraries handle communication protocols. `Wire.h` is used for I2C communication with the MPU6050 sensor.
- **Servo.h**: This library is used to control the two servos.
- **math.h**: Provides mathematical functions such as `atan2()` and `sqrt()` for calculating angles (pitch and roll).

```cpp
#define MPU_ADDRESS 0x68  // I2C address of the MPU-6050
```
- Defines the I2C address for the MPU6050 sensor (0x68). This allows the code to communicate with the sensor.

## 2. **Servo Setup and Data Structuring**:
```cpp
Servo servoX, servoY;
```
- These two `Servo` objects, `servoX` and `servoY`, control the servos that adjust based on the sensor data for **roll** and **pitch**.

```cpp
struct AccelData {
    int16_t x;
    int16_t y;
    int16_t z;
};
```
- `AccelData` is a `struct` that groups accelerometer data (`x`, `y`, `z` axes). Using this structure makes it cleaner to pass around accelerometer readings in the code.

```cpp
AccelData accelData;
```
- A single instance of the `AccelData` struct to hold real-time data from the accelerometer. It stores `x`, `y`, and `z` values that are updated from the MPU sensor in the loop.

## 3. **Function Prototypes**:
Before `setup()`, function prototypes are declared to tell the compiler what functions will be used. This is a common practice in C/C++ to improve readability and structure:
```cpp
void initializeMPU();
void readAccelData(AccelData &data);
int calculatePitchRoll(int16_t a, int16_t b, int16_t c);
void controlServos(int pitch, int roll);
```

## 4. **Setup Function**:
```cpp
void setup() {
    Serial.begin(9600);
    
    servoX.attach(8);
    servoY.attach(9);

    initializeMPU();
}
```
- **Serial.begin(9600)**: Initializes serial communication at a baud rate of 9600, so you can see the output via the serial monitor.
- **servoX.attach(8)** and **servoY.attach(9)**: Connects the two servos to digital pins 8 and 9, respectively.
- **initializeMPU()**: Initializes the MPU6050 sensor, which is explained next.

## 5. **MPU Initialization**:
```cpp
void initializeMPU() {
    Wire.begin();
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x6B);  // Access power management register
    Wire.write(0);     // Wake up MPU-6050 by setting the register to 0
    Wire.endTransmission(true);
    delay(100);
}
```
- **Wire.begin()**: Starts I2C communication.
- **Wire.beginTransmission()**: Starts communication with the MPU6050 at its defined address.
- **Wire.write(0x6B)**: Accesses the MPU6050's power management register.
- **Wire.write(0)**: Wakes up the MPU6050 (it’s in sleep mode by default).
- **delay(100)**: Gives the sensor time to stabilize after waking up.

## 6. **Main Loop Function**:
```cpp
void loop() {
    readAccelData(accelData);

    int roll = calculatePitchRoll(accelData.x, accelData.y, accelData.z);
    int pitch = calculatePitchRoll(accelData.y, accelData.x, accelData.z);

    controlServos(pitch, roll);

    Serial.print("Pitch: ");
    Serial.print(pitch);
    Serial.print("\tRoll: ");
    Serial.println(roll);

    delay(100);
}
```
- **readAccelData(accelData)**: Calls the function that reads the MPU6050 data into the `accelData` struct.
- **calculatePitchRoll()**: This function computes the **pitch** and **roll** based on accelerometer values. It's called twice: once for `roll` using `x`, `y`, `z` values, and once for `pitch` using `y`, `x`, `z`.
- **controlServos(pitch, roll)**: The calculated `pitch` and `roll` values are used to control the servos.
- **Serial.print()**: Displays the pitch and roll values in the serial monitor for debugging.

## 7. **Reading Accelerometer Data**:
```cpp
void readAccelData(AccelData &data) {
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B);  // Start reading from ACCEL_XOUT_H register
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDRESS, 6, true);  // Request 6 bytes of accelerometer data
    
    data.x = (Wire.read() << 8) | Wire.read();  // ACCEL_XOUT_H and ACCEL_XOUT_L
    data.y = (Wire.read() << 8) | Wire.read();  // ACCEL_YOUT_H and ACCEL_YOUT_L
    data.z = (Wire.read() << 8) | Wire.read();  // ACCEL_ZOUT_H and ACCEL_ZOUT_L
}
```
- **Wire.beginTransmission()**: Starts communication with the MPU6050.
- **Wire.write(0x3B)**: Points to the first accelerometer data register (ACCEL_XOUT_H).
- **Wire.requestFrom()**: Requests 6 bytes of data from the MPU6050 (2 bytes each for `x`, `y`, and `z` axes).
- **data.x = (Wire.read() << 8) | Wire.read()**: Combines two 8-bit values into a 16-bit value. This process is repeated for `y` and `z`.

## 8. **Calculating Pitch and Roll**:
```cpp
int calculatePitchRoll(int16_t a, int16_t b, int16_t c) {
    double b_squared = (double)(b * b) + (double)(c * c);
    double result = atan2((double)a, sqrt(b_squared)) * (180.0 / M_PI);
    return (int)result;
}
```
- **atan2()**: A mathematical function that calculates the angle (in radians) between the `a` axis and the hypotenuse formed by `b` and `c`. 
- **sqrt()**: Computes the square root of the sum of squares of `b` and `c`.
- **(180.0 / M_PI)**: Converts the angle from radians to degrees. 
- This function returns the angle for either pitch or roll based on accelerometer data.

## 9. **Controlling the Servos**:
```cpp
void controlServos(int pitch, int roll) {
    int servoRoll = map(roll, -90, 90, 0, 179);
    int servoPitch = map(pitch, -90, 90, 179, 0);
    
    servoX.write(servoRoll);
    servoY.write(servoPitch);
}
```
- **map()**: Maps the calculated `roll` and `pitch` angles (ranging from -90° to 90°) to values between 0 and 179, which are suitable for controlling the servos.
  - For `roll`, `0` represents -90°, and `179` represents +90°.
  - For `pitch`, `0` represents +90°, and `179` represents -90°.
- **servoX.write()** and **servoY.write()**: Set the servo positions based on the calculated and mapped values.

---

## In Summary:
- The MPU6050 provides raw accelerometer data for the X, Y, and Z axes.
- The accelerometer data is processed to calculate pitch and roll angles using trigonometric functions (`atan2`).
- These calculated angles are then mapped to servo angles (0-179°), which control the servo positions, adjusting them to stabilize the system based on pitch and roll data.
- Throughout the loop, this process is repeated, continuously updating the servo positions in real time based on accelerometer data.

This structure efficiently separates the concerns (MPU setup, data reading, servo control), improving the readability and maintainability of the code while ensuring the system behaves predictably.