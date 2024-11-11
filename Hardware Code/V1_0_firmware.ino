// Load the libraries
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SD.h>       
#include <SPI.h>               

// Create the LCD instance
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display
unsigned long lcd_refresh_time = 5000;

// Create the file instance
File myFile;

// Create the custom LCD symbol for '/'
uint8_t SpecialChar [8]= { 0x00, 0x10, 0x08, 0x04, 0x02, 0x01, 0x00, 0x00 };

// Pin used to control the LED pwm
int ledPin = 13; 

// For the SD Card
const int _MISO = 4;
const int _MOSI = 7;
const int _CS = 5;
const int _SCK = 6;

void setup() {
  // Turn off the LED
  analogWrite(ledPin, 0);

  // Declare the pins 20 and 21 as SDA and SCL
  Wire.setSDA(20);
  Wire.setSCL(21);
  Wire.begin();

  // Configure the SD
  SPI.setRX(_MISO);
  SPI.setTX(_MOSI);
  SPI.setSCK(_SCK);

  // Initiate the LCD and create the special character '/'
  lcd.init();     
  lcd.backlight();
  lcd.createChar(0, SpecialChar);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("V1.0");
  delay(5000);

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Opening SD Card");
  delay(5000);

  // Initiate the SD
  if (!SD.begin(_CS)) {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("SD Failed");
    delay(20000);
  }
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("SD Ready");
  lcd.setCursor(0,1);
  lcd.print("Reading...");
  delay(5000);
}

void loop() {
  // Variables
  float STEP_SIZE;
  int PROGRAM_DURATION;
  int magnitude;
  int PROGRAM_COUNTS;
  int counter = 1;
  unsigned long reference_time = millis();

  // Load the SD card and read the first couple of values
  myFile = SD.open("data.txt");
  STEP_SIZE = myFile.parseFloat();
  float PROGRAM_DELAY_MICROSECONDS = STEP_SIZE * 1000;
  PROGRAM_DURATION = myFile.parseInt();
  PROGRAM_COUNTS = myFile.parseInt();

  // Display the loaded values
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Step: ");
  lcd.print(STEP_SIZE);
  lcd.setCursor(0, 1);
  lcd.print(PROGRAM_DURATION);
  lcd.print("s");
  delay(5000);

  // Main loop for fading
  while (myFile.available()) {
    magnitude = myFile.parseInt();
    analogWrite(ledPin, magnitude);
    if (millis() - reference_time >= lcd_refresh_time) {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print(counter);
      lcd.print(" ");
      lcd.print(char(0));
      lcd.print(" ");
      lcd.print(PROGRAM_COUNTS);
      lcd.setCursor(0,1);
      lcd.print("Intensity: ");
      lcd.print(magnitude);
      reference_time = millis();
    }
    counter++;
    delay(PROGRAM_DELAY_MICROSECONDS);
  }
  analogWrite(ledPin, 0);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Done.");
  delay(60000);
}
