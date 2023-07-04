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


class PyClock:
    def __init__(self):
        spi =  busio.SPI(clock=board.GP18, MOSI=board.GP19)
        cs = digitalio.DigitalInOut(board.GP17)
        self.matrix = matrices.CustomMatrix(width=32, height=8, spi=spi, cs=cs)
        wifi.radio.connect(secrets.ssid, secrets.password)
        self.pool = socketpool.SocketPool(wifi.radio)

    def run(self):
        self.blink()
        while True:
            self.update_clock()

    def to_cest(self, h):
        cest_h = int(h) + 2
        if cest_h > 23:
            cest_h = cest_h - 24
        return str(cest_h)

    def update_clock(self):
        try:
            h, m, s = self.now().split(' ')[2].split(':')
            h = self.to_cest(h)
            self.print(f"{h}:{m}")
            time.sleep(60 - int(s))
        except RequestError:
            self.print("Error")
            time.sleep(30)

    def print(text, x=1, y=1):
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

    def now(self):
        try:
            s = self.pool.socket()
            s.connect(("time.nist.gov", 13))
            result = bytearray(51)
            s.recv_into(result)
        except Exception as e:
            raise RequestError() from e
        finally:
            s.close()
        return result.decode()


if __name__ == "__main__":
    clock = PyClock()
    clock.run()
