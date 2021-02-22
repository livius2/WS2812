class WS2812:
    def __init__(self, pin, channel=3):
        from machine import RMT
        self.rmt = RMT(channel=channel, gpio=pin, tx_idle_level=0)

    def show(self, data):
        from time import sleep_us
        duration = bytearray(len(data) * 24 * 2)
        index = 0
        for pixel in data:
            for byte in pixel:
                mask = 0x80
                while mask:
                    duration[index:index+2] = \
                        b'\x08\x04' if byte & mask else b'\x04\x08'
                    index += 2
                    mask >>= 1
        sleep_us(60)  # wait for the reset time
        self.rmt.pulses_send(tuple(duration), (1, 0) * (len(data) * 24))


class WS2812_immutable:
    def __init__(self, pixel_count, pin, channel=3):
        from machine import RMT
        self.rmt = RMT(channel=channel, gpio=pin, tx_idle_level=0)
		self.pixel_count = pixel_count
		self.duration = bytearray(pixel_count * 24 * 2)
		self.pulse_data = (1, 0) * (pixel_count * 24)

    def show(self, data):
        from time import sleep_us
        if len(data)!=self.pixel_count:
            raise ValueError("Param 'data' have wrong size. Expected: " + str(self.pixel_count) + " but is: " + str(len(data)))
        index = 0
        for pixel in data:
            for byte in pixel:
                mask = 0x80
                while mask:
                    self.duration[index:index+2] = \
                        b'\x08\x04' if byte & mask else b'\x04\x08'
                    index += 2
                    mask >>= 1
        sleep_us(60)  # wait for the reset time
        self.rmt.pulses_send(tuple(self.duration), self.pulse_data)
