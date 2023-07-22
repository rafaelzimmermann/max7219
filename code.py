import time
import board
import busio
import digitalio
import wifi
import socketpool

from secrets import secrets
from libs import matrices


class RequestError(Exception):
   pass

class Time:
    def __init__(self, hour, minute, second):
        self._hour = int(hour)
        self._minute = int(minute)
        self._second = int(second)

    def to_cest(self):
        cest_h = self._hour + 2
        if cest_h > 23:
            cest_h = cest_h - 24
        return Time(cest_h, self._minute, self._second)

    def increment(self, minutes: int):
        self._minute += minutes % 60
        self._hour += int(minutes / 60)
        self._second = 0

    @staticmethod
    def _zero_padded(value):
        return str(value + 100)[-2:]

    @property
    def str_h(self):
        return self._zero_padded(self._hour)

    @property
    def str_m(self):
        return self._zero_padded(self._minute)

    @property
    def str_s(self):
        return self._zero_padded(self._second)
    
    @property
    def hour(self):
        return self._hour
    
    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    def __str__(self):
        return f"{self.str_h}:{self.str_m}"


class PyClock:
    def __init__(self):
        spi =  busio.SPI(clock=board.GP18, MOSI=board.GP19)
        cs = digitalio.DigitalInOut(board.GP17)
        self.matrix = matrices.CustomMatrix(width=32, height=8, spi=spi, cs=cs)
        wifi.radio.connect(secrets.ssid, secrets.password)
        self.pool = socketpool.SocketPool(wifi.radio)
        self.current_time = self.now()

    def run(self):
        self.blink()
        while True:
            if self.current_time.minute % 10 == 0:
                self.current_time = self.now()
            self.update_clock()
            time.sleep(60 - self.current_time.second)
            self.current_time.increment(1)
            
    def update_clock(self):
        try:
            self.matrix.fill(0)
            for i, c in enumerate(str(self.current_time).replace(":", "")):
                if i > 1:
                    self.matrix.text(c, 2 + (i* 8), 1)
                else:
                    self.matrix.text(c, 1 + (i* 8), 1)
            self.matrix.pixel(15, 3, 1)
            self.matrix.pixel(16, 3, 1)
            self.matrix.pixel(15, 5, 1)
            self.matrix.pixel(16, 5, 1)
            self.matrix.show()
        except RequestError as e:
            print(e)
            self.print("Error")
            time.sleep(30)

    def print(self, text, x=1, y=1):
        self.matrix.fill(0)
        self.matrix.text(text, x, y)
        self.matrix.show()

    def fill_and_show(self, value):
        self.matrix.fill(value)
        self.matrix.show()
        time.sleep(0.5)

    def blink(self):
        self.fill_and_show(True)
        self.fill_and_show(False)

    def now(self) -> Time:
        try:
            s = self.pool.socket()
            s.connect(("time.nist.gov", 13))
            result = bytearray(51)
            s.recv_into(result)
            parts = result.decode().split(' ')[2].split(':')
            return Time(hour=parts[0], minute=parts[1], second=parts[2]).to_cest()
        except Exception as e:
            raise RequestError(e) from e
        finally:
            s.close()
        return result.decode()


if __name__ == "__main__":
    clock = PyClock()
    clock.run()
