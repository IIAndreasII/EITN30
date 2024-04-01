from RF24 import RF24, RF24_PA_LOW, RF24_1MBPS

# Setup for GPIO pins (CE, CSN) on the Raspberry Pi
# CE pin on GPIO17, CSN pin on GPIO0 (using spidev0.0)
ce_pin_0 = 8
csn_pin_0 = 0

ce_pin_1 = 7
csn_pin_1 = 0

# Initialize the RF24 object with the CE and CSN pin numbers
radio = RF24(ce_pin_0, csn_pin_0)


# Begin operation of the radio module
if not radio.begin():
    raise RuntimeError("NRF24L01+ hardware is not responding")

# Set the PA Level (Power Amplifier Level)
radio.setPALevel(RF24_PA_LOW)  # Options are MIN, LOW, HIGH, MAX

# Set the data rate
radio.setDataRate(RF24_1MBPS)  # Options are 1MBPS, 2MBPS, 250KBPS

# Set the RF communication channel (0-125, 2.4GHz to 2.525GHz)
radio.setChannel(76)

# Optionally, you can enable dynamic payloads and auto-acknowledgment features
radio.enableDynamicPayloads()
radio.enableAckPayload()

# Print out the configuration for verification
print("NRF24L01+ configured successfully!")
print(f"PA Level: {radio.getPALevel()}")
print(f"Data Rate: {radio.getDataRate()}")
print(f"Channel: {radio.getChannel()}")