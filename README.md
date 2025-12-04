# RGB Binary Clock With RTC and TM1637 Display (MicroPython)

This project is a multi-display real-time clock built using a microcontroller running MicroPython, a DS3231 high-accuracy RTC, multiple 74HC595-style shift register LED outputs, and a TM1637 4-digit 7-segment display.

Time is displayed simultaneously in:
- RGB LED binary format for hours and minutes
- Red LED binary format for seconds
- Standard numeric format on a 7-segment display

The system runs fully offline using the DS3231 hardware RTC and maintains accurate time even during power loss.

This project demonstrates low-level GPIO control, I2C RTC integration, custom display drivers, bit-level shift register control, and real-time timing synchronization.

---

## Core Features

- Hardware RTC timekeeping using DS3231
- RGB LED binary time display
- Dedicated red LED binary seconds display
- TM1637 4-digit 7-segment HH:MM display
- Direct shift register control via GPIO
- MicroPython implementation
- Accurate 1-second update timing
- Independent color channels for hours and minutes
- Automatic LED bank reset on boot

---

## Display Logic

- Hours are displayed using RGB LEDs through shift registers
- Minutes are displayed using RGB LEDs through shift registers
- Seconds are displayed using red LEDs only
- TM1637 shows standard digital time in HHMM format
- LED banks rotate through color channels:
  - Hours rotate through RGB based on hour modulo 3
  - Minutes rotate through RGB based on 20-minute intervals
- Shift registers output raw binary values of time

---

## Hardware Used

- Microcontroller running MicroPython
- DS3231 RTC module
- TM1637 4-digit 7-segment display
- Shift registers (74HC595 or equivalent)
- RGB LED arrays
- Red LED array for seconds
- External power supply for LEDs

---

## Pin Assignments

### DS3231 RTC (I2C)

- SDA → GPIO 0  
- SCL → GPIO 1  

### TM1637 Display

- CLK → GPIO 26  
- DIO → GPIO 27  

---

## Shift Register Pin Mapping

### Hours (RGB)

Red  
- LATCH → GPIO 2  
- CLOCK → GPIO 3  
- DATA  → GPIO 4  

Green  
- LATCH → GPIO 5  
- CLOCK → GPIO 6  
- DATA  → GPIO 7  

Blue  
- LATCH → GPIO 8  
- CLOCK → GPIO 9  
- DATA  → GPIO 10  

### Minutes (RGB)

Red  
- LATCH → GPIO 11  
- CLOCK → GPIO 12  
- DATA  → GPIO 13  

Green  
- LATCH → GPIO 14  
- CLOCK → GPIO 15  
- DATA  → GPIO 16  

Blue  
- LATCH → GPIO 17  
- CLOCK → GPIO 18  
- DATA  → GPIO 19  

### Seconds (Red Only)

- LATCH → GPIO 20  
- CLOCK → GPIO 21  
- DATA  → GPIO 22  

---

## Time Source

- DS3231 RTC provides:
  - Seconds
  - Minutes
  - Hours
  - Day
  - Date
  - Month
  - Year
- Time is stored in BCD format and converted to standard integers in firmware

---

## Firmware Details

- Written entirely in MicroPython
- Includes:
  - Custom TM1637 driver class
  - Custom DS3231 driver class
  - Bitwise shift register handling
  - Manual binary LED display logic
- Runs a precise 1 Hz update loop using millisecond ticks
- Busy-wait timing ensures consistent frame synchronization

---

## Initialization Behavior

- All shift register outputs are reset on power-up
- RTC time can be manually set in firmware
- Displays immediately synchronize on startup
- TM1637 brightness is software controlled

---

## How It Works

1. RTC is initialized via I2C.
2. Current time is read once per second.
3. Binary values of hours, minutes, and seconds are computed.
4. LED shift registers output the corresponding binary LED patterns.
5. TM1637 updates the numeric HHMM display.
6. RGB color banks rotate automatically based on time position.

---

## Software Requirements

- MicroPython firmware installed on the target board
- No external libraries required beyond standard MicroPython

---

## Setting the Time

Modify this line in the firmware before deployment:
rtc.datetime((2024, 8, 4, 1, 17, 36, 0))

