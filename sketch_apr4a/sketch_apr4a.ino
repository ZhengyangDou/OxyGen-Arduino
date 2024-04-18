#include <SparkFun_SGP30_Arduino_Library.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h> 
#include <DHT11.h>
SGP30 mySensor; 
LiquidCrystal_I2C lcd(0x27, 16, 2); 
const float MAX_CO2 = 40000.0;
const float MAX_TVOC = 60000.0;
DHT11 dht11(2);
void setup() {
  Serial.begin(9600);
  Wire.begin();
  lcd.init(); // Initialize the LCD
  lcd.backlight(); 
  lcd.clear(); 
  if (mySensor.begin() == false) {
    Serial.println("No SGP30 Detected. Check connections.");
    while (1);
  }

  mySensor.initAirQuality();
}

void loop() {
  
  mySensor.measureAirQuality();
  int temperature = 0;
  int humidity = 0;
  int result = dht11.readTemperatureHumidity(temperature, humidity);
  float co2_percentage = (mySensor.CO2 / MAX_CO2) * 100;
  float tvoc_percentage = (mySensor.TVOC / MAX_TVOC) * 100;
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("CO2:");
  lcd.print(int(co2_percentage));
  lcd.print("%");
  lcd.print(" TEMP:");
  lcd.print(int(temperature));
  lcd.print("");
  lcd.setCursor(0, 1);
  lcd.print("TVOC:");
  lcd.print(int(tvoc_percentage));
  lcd.print("%");
  lcd.print(" Rh:");
  lcd.print(int(humidity));
  lcd.print("%");
  Serial.print(co2_percentage);
  Serial.print(" ");
  Serial.print(tvoc_percentage);
  Serial.print(" ");
  Serial.print(temperature);
  Serial.print(" ");
  Serial.println(humidity);
}
