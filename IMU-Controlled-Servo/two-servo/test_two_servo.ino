#include <SPI.h>
#include <Wire.h>
#include <Servo.h>
#include <math.h>

#define MPU_ADDRESS 0x68  // I2C address of the MPU-6050

Servo servoX, servoY;

// MPU-6050 Accelerometer readings
struct AccelData {
    int16_t x;
    int16_t y;
    int16_t z;
};

AccelData accelData;

// Function Prototypes
void initializeMPU();
void readAccelData(AccelData &data);
int calculatePitchRoll(int16_t a, int16_t b, int16_t c);
void controlServos(int pitch, int roll);

void setup() {
    Serial.begin(9600);
    
    // Attach servos to respective pins
    servoX.attach(8);
    servoY.attach(9);

    // Initialize the MPU-6050
    initializeMPU();
}

void loop() {
    // Read accelerometer data from MPU-6050
    readAccelData(accelData);

    // Calculate Roll and Pitch based on accelerometer data
    int roll = calculatePitchRoll(accelData.x, accelData.y, accelData.z);
    int pitch = calculatePitchRoll(accelData.y, accelData.x, accelData.z);

    // Map calculated pitch and roll to servo positions and control servos
    controlServos(pitch, roll);

    // Debug output to the serial monitor
    Serial.print("Pitch: ");
    Serial.print(pitch);
    Serial.print("\tRoll: ");
    Serial.println(roll);

    delay(100);  // Adding a small delay for better serial output visibility
}

// Function to initialize MPU-6050
void initializeMPU() {
    Wire.begin();
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x6B);  // Access power management register
    Wire.write(0);     // Wake up MPU-6050 by setting the register to 0
    Wire.endTransmission(true);
    delay(100);  // Allow the MPU to stabilize after waking up
}

// Function to read accelerometer data from MPU-6050
void readAccelData(AccelData &data) {
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B);  // Start reading from ACCEL_XOUT_H register
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDRESS, 6, true);  // Request 6 bytes of accelerometer data
    
    data.x = (Wire.read() << 8) | Wire.read();  // ACCEL_XOUT_H and ACCEL_XOUT_L
    data.y = (Wire.read() << 8) | Wire.read();  // ACCEL_YOUT_H and ACCEL_YOUT_L
    data.z = (Wire.read() << 8) | Wire.read();  // ACCEL_ZOUT_H and ACCEL_ZOUT_L
}

// Function to calculate pitch or roll based on accelerometer data
int calculatePitchRoll(int16_t a, int16_t b, int16_t c) {
    double b_squared = (double)(b * b) + (double)(c * c);
    double result = atan2((double)a, sqrt(b_squared)) * (180.0 / M_PI);
    return (int)result;
}

// Function to control servos based on pitch and roll calculations
void controlServos(int pitch, int roll) {
    // Map pitch and roll values to servo ranges (0-179 degrees)
    int servoRoll = map(roll, -90, 90, 0, 179);
    int servoPitch = map(pitch, -90, 90, 179, 0);
    
    // Set servo positions
    servoX.write(servoRoll);
    servoY.write(servoPitch);
}
