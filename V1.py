from machine import Pin, I2C
import utime

# TM1637 Library
class TM1637:
    TM1637_CMD1 = 0x40  # data command
    TM1637_CMD2 = 0xC0  # address command
    TM1637_CMD3 = 0x80  # display control command
    TM1637_DSP_ON = 0x88
    TM1637_DELAY = 10  # us

    _SEGMENTS = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71]

    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        self.clk.init(Pin.OUT)
        self.dio.init(Pin.OUT)
        self._brightness = self.TM1637_DSP_ON | 7
        self.off()

    def _start(self):
        self.dio(0)
        utime.sleep_us(self.TM1637_DELAY)
        self.clk(0)
        utime.sleep_us(self.TM1637_DELAY)

    def _stop(self):
        self.clk(0)
        utime.sleep_us(self.TM1637_DELAY)
        self.dio(0)
        utime.sleep_us(self.TM1637_DELAY)
        self.clk(1)
        utime.sleep_us(self.TM1637_DELAY)
        self.dio(1)

    def _write_data(self, data):
        for bit in range(8):
            self.dio((data >> bit) & 1)
            self.clk(1)
            utime.sleep_us(self.TM1637_DELAY)
            self.clk(0)
            utime.sleep_us(self.TM1637_DELAY)
        self.clk(1)
        utime.sleep_us(self.TM1637_DELAY)
        self.clk(0)
        utime.sleep_us(self.TM1637_DELAY)

    def _write_cmd(self, cmd):
        self._start()
        self._write_data(cmd)
        self._stop()

    def on(self):
        self._write_cmd(self._brightness)

    def off(self):
        self._write_cmd(self.TM1637_DSP_ON)

    def brightness(self, val=None):
        if val is None:
            return self._brightness & 0x07
        self._brightness = self.TM1637_DSP_ON | (val & 0x07)
        self.on()

    def write(self, segments, pos=0):
        self._write_cmd(self.TM1637_CMD1)
        self._start()
        self._write_data(self.TM1637_CMD2 | pos)
        for seg in segments:
            self._write_data(seg)
        self._stop()
        self.on()

    def encode_digit(self, digit):
        return self._SEGMENTS[digit & 0x0f]

    def encode_string(self, string):
        segments = []
        for char in string:
            if char == ' ':
                segments.append(0x00)
            elif '0' <= char <= '9':
                segments.append(self._SEGMENTS[ord(char) - ord('0')])
            else:
                segments.append(0x00)
        return segments

# DS3231 RTC Library
class DS3231:
    DS3231_I2C_ADDR = 0x68

    def __init__(self, i2c):
        self.i2c = i2c

    def _bcd2bin(self, value):
        return (value & 0x0F) + ((value >> 4) * 10)

    def _bin2bcd(self, value):
        return (value // 10 << 4) + (value % 10)

    def datetime(self, dt=None):
        if dt is None:
            data = self.i2c.readfrom_mem(self.DS3231_I2C_ADDR, 0x00, 7)
            print(f"Raw I2C data: {data}")  # Debug print
            return (self._bcd2bin(data[0]), self._bcd2bin(data[1]), self._bcd2bin(data[2]),
                    self._bcd2bin(data[3]), self._bcd2bin(data[4]), self._bcd2bin(data[5]), self._bcd2bin(data[6]))
        else:
            data = bytearray(7)
            data[0] = self._bin2bcd(dt[6])  # Seconds
            data[1] = self._bin2bcd(dt[5])  # Minutes
            data[2] = self._bin2bcd(dt[4])  # Hours
            data[3] = self._bin2bcd(dt[3])  # Day
            data[4] = self._bin2bcd(dt[2])  # Date
            data[5] = self._bin2bcd(dt[1])  # Month
            data[6] = self._bin2bcd(dt[0])  # Year
            self.i2c.writeto_mem(self.DS3231_I2C_ADDR, 0x00, data)

# Define I2C pins for DS3231 RTC
I2C_SCL = Pin(1, Pin.OUT)
I2C_SDA = Pin(0, Pin.OUT)
i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA)

# Initialize DS3231
rtc = DS3231(i2c)

# Initialize TM1637
tm = TM1637(clk=Pin(26), dio=Pin(27))

# Set the RTC time (Year, Month, Date, Day, Hour, Minute, Second)
# Update the time to your current local time
rtc.datetime((2024, 8, 4, 1, 17, 36, 0))

# Define shift register pins for hours (counts to 24)
LATCH_PIN_HOUR_RED = Pin(2, Pin.OUT)
CLOCK_PIN_HOUR_RED = Pin(3, Pin.OUT)
DATA_PIN_HOUR_RED = Pin(4, Pin.OUT)

LATCH_PIN_HOUR_GREEN = Pin(5, Pin.OUT)
CLOCK_PIN_HOUR_GREEN = Pin(6, Pin.OUT)
DATA_PIN_HOUR_GREEN = Pin(7, Pin.OUT)

LATCH_PIN_HOUR_BLUE = Pin(8, Pin.OUT)
CLOCK_PIN_HOUR_BLUE = Pin(9, Pin.OUT)
DATA_PIN_HOUR_BLUE = Pin(10, Pin.OUT)

# Define shift register pins for minutes (counts to 60)
LATCH_PIN_MINUTES_RED = Pin(11, Pin.OUT)
CLOCK_PIN_MINUTES_RED = Pin(12, Pin.OUT)
DATA_PIN_MINUTES_RED = Pin(13, Pin.OUT)

LATCH_PIN_MINUTES_GREEN = Pin(14, Pin.OUT)
CLOCK_PIN_MINUTES_GREEN = Pin(15, Pin.OUT)
DATA_PIN_MINUTES_GREEN = Pin(16, Pin.OUT)

LATCH_PIN_MINUTES_BLUE = Pin(17, Pin.OUT)
CLOCK_PIN_MINUTES_BLUE = Pin(18, Pin.OUT)
DATA_PIN_MINUTES_BLUE = Pin(19, Pin.OUT)

# Define shift register pins for seconds (counts to 60) with red LEDs only
LATCH_PIN_SECONDS_RED = Pin(20, Pin.OUT)
CLOCK_PIN_SECONDS_RED = Pin(21, Pin.OUT)
DATA_PIN_SECONDS_RED = Pin(22, Pin.OUT)

def update_shift_register(latch_pin, clock_pin, data_pin, value):
    latch_pin.value(0)
    for i in range(8):
        clock_pin.value(0)
        data_pin.value((value >> (7 - i)) & 1)
        clock_pin.value(1)
    latch_pin.value(1)

def reset_leds(latch_pins, clock_pins, data_pins):
    for latch_pin, clock_pin, data_pin in zip(latch_pins, clock_pins, data_pins):
        update_shift_register(latch_pin, clock_pin, data_pin, 0)

def display_time(seconds_latch_pin, seconds_clock_pin, seconds_data_pin, 
                 minutes_latch_pins, minutes_clock_pins, minutes_data_pins, 
                 hours_latch_pins, hours_clock_pins, hours_data_pins):
    
    last_hour_color_index = -1
    last_minute_color_index = -1

    while True:
        start_time = utime.ticks_ms()
        
        # Get current time from DS3231
        try:
            now = rtc.datetime()
            print(f"RTC datetime: {now}")  # Debug print
            seconds, minutes, hours = now[0], now[1], now[2]
        except Exception as e:
            print(f"Error reading time: {e}")
            continue

        # Calculate hour and minute color indices
        hours_color_index = hours % 3
        minutes_color_index = (minutes // 20) % 3

        # Clear hour LEDs if the color index has changed
        if hours_color_index != last_hour_color_index:
            reset_leds(hours_latch_pins, hours_clock_pins, hours_data_pins)
            last_hour_color_index = hours_color_index

        # Clear minute LEDs if the color index has changed
        if minutes_color_index != last_minute_color_index:
            reset_leds(minutes_latch_pins, minutes_clock_pins, minutes_data_pins)
            last_minute_color_index = minutes_color_index

        # Display seconds with red LEDs
        update_shift_register(seconds_latch_pin, seconds_clock_pin, seconds_data_pin, seconds)
        
        # Display minutes with red, green, blue LEDs
        update_shift_register(minutes_latch_pins[minutes_color_index], minutes_clock_pins[minutes_color_index], minutes_data_pins[minutes_color_index], minutes)
        
        # Display hours with red, green, blue LEDs
        update_shift_register(hours_latch_pins[hours_color_index], hours_clock_pins[hours_color_index], hours_data_pins[hours_color_index], hours)

        # Update 4-digit 7-segment display
        tm.write(tm.encode_string(f"{hours:02d}{minutes:02d}"))

        print(f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")  # Print the values for debugging
        while utime.ticks_diff(utime.ticks_ms(), start_time) < 1000:
            pass  # Busy wait for the remaining time to ensure exactly 1 second delay

def main():
    # Reset all LEDs when powered up
    reset_leds(
        [LATCH_PIN_HOUR_RED, LATCH_PIN_HOUR_GREEN, LATCH_PIN_HOUR_BLUE],
        [CLOCK_PIN_HOUR_RED, CLOCK_PIN_HOUR_GREEN, CLOCK_PIN_HOUR_BLUE],
        [DATA_PIN_HOUR_RED, DATA_PIN_HOUR_GREEN, DATA_PIN_HOUR_BLUE]
    )
    reset_leds(
        [LATCH_PIN_MINUTES_RED, LATCH_PIN_MINUTES_GREEN, LATCH_PIN_MINUTES_BLUE],
        [CLOCK_PIN_MINUTES_RED, CLOCK_PIN_MINUTES_GREEN, CLOCK_PIN_MINUTES_BLUE],
        [DATA_PIN_MINUTES_RED, DATA_PIN_MINUTES_GREEN, DATA_PIN_MINUTES_BLUE]
    )
    reset_leds(
        [LATCH_PIN_SECONDS_RED],
        [CLOCK_PIN_SECONDS_RED],
        [DATA_PIN_SECONDS_RED]
    )

    # Pins for the "seconds" (counts to 60) with red LEDs only
    seconds_latch_pin = LATCH_PIN_SECONDS_RED
    seconds_clock_pin = CLOCK_PIN_SECONDS_RED
    seconds_data_pin = DATA_PIN_SECONDS_RED

    # Pins for the "minutes" (counts to 60) with red, green, blue LEDs
    minutes_latch_pins = [LATCH_PIN_MINUTES_RED, LATCH_PIN_MINUTES_GREEN, LATCH_PIN_MINUTES_BLUE]
    minutes_clock_pins = [CLOCK_PIN_MINUTES_RED, CLOCK_PIN_MINUTES_GREEN, CLOCK_PIN_MINUTES_BLUE]
    minutes_data_pins = [DATA_PIN_MINUTES_RED, DATA_PIN_MINUTES_GREEN, DATA_PIN_MINUTES_BLUE]

    # Pins for the "hours" (counts to 24) with red, green, blue LEDs
    hours_latch_pins = [LATCH_PIN_HOUR_RED, LATCH_PIN_HOUR_GREEN, LATCH_PIN_HOUR_BLUE]
    hours_clock_pins = [CLOCK_PIN_HOUR_RED, CLOCK_PIN_HOUR_GREEN, CLOCK_PIN_HOUR_BLUE]
    hours_data_pins = [DATA_PIN_HOUR_RED, DATA_PIN_HOUR_GREEN, DATA_PIN_HOUR_BLUE]

    display_time(seconds_latch_pin, seconds_clock_pin, seconds_data_pin,
                 minutes_latch_pins, minutes_clock_pins, minutes_data_pins,
                 hours_latch_pins, hours_clock_pins, hours_data_pins)

main()
