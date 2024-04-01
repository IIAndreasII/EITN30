class SPI:
    mosi_pin = -1
    miso_pin = -1
    sclk_pin = -1
    ce_pin   = -1

    def __init__(self, mosi, miso, sclk, ce):
        self.mosi_pin = mosi
        self.miso_pin = miso
        self.sclk = sclk
        self.ce_pin = ce