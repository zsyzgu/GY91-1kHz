/*
 * VDD ---------------------- 3.3V
 * SDA ----------------------- A4
 * SCL ----------------------- A5
 * GND ---------------------- GND
 */
#include "MPU9250.h"

MPU9250 mpu = MPU9250();
long *t;
int16_t *ax, *ay, *az, *gx, *gy, *gz;
bool* is_touch;
byte buf[17];

#include <CapacitiveSensor.h>
int ledPin = 13;
CapacitiveSensor cs_4_2 = CapacitiveSensor(4,2);
void updateTouch() {
  long cap =  cs_4_2.capacitiveSensor(2);
  if (cap > 15) {
    digitalWrite(ledPin, HIGH);
    *is_touch = true;
  } else {
    digitalWrite(ledPin, LOW);
    *is_touch = false;
  }
}

void setup(void) {
  Serial.begin(250000);  
  uint8_t temp = mpu.begin();
  mpu.set_accel_range(RANGE_8G);
  mpu.set_gyro_range(RANGE_GYRO_500);
  t = (long*)&buf[0];
  ax = (int16_t*)&buf[4];
  ay = (int16_t*)&buf[6];
  az = (int16_t*)&buf[8];
  gx = (int16_t*)&buf[10];
  gy = (int16_t*)&buf[12];
  gz = (int16_t*)&buf[14];
  is_touch = (bool*)&buf[16];
  pinMode(ledPin, OUTPUT);
  delay(1000);
}

void loop() {
  *t = micros();
  mpu.get_accel();
  *ax = mpu.x;
  *ay = mpu.y;
  *az = mpu.z;
  mpu.get_gyro();
  *gx = mpu.gx;
  *gy = mpu.gy;
  *gz = mpu.gz;
  Serial.write(buf, 17);
  //updateTouch();
  while (micros() - (*t) < 1000);
}
