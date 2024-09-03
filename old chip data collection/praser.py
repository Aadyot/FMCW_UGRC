import struct

class FrameParser:
    FUNCTION_CODES = {
        0x01: "Read Command",
        0x02: "Write Command",
        0x03: "Passive Report Command",
        0x04: "Active Report Command",
    }

    def __init__(self, frame_str):
        self.frame = self.convert_frame_to_bytes(frame_str)
        self.header = None
        self.length = None
        self.function_code = None
        self.address_1 = None
        self.address_2 = None
        self.data = None
        # self.checksum = None
        self.parse_frame()

    def convert_frame_to_bytes(self, frame_str):
        # Split the string by spaces and convert each hex value to a byte
        hex_values = frame_str.strip().split()
        return bytes(int(value, 16) for value in hex_values)

    def parse_frame(self):
        if len(self.frame) < 8:  # Minimum length check
            raise ValueError("Frame is too short")

        # Start code (Header): 1 Byte, fixed to 0x55
        self.header = self.frame[0]
        if self.header != 0x55:
            raise ValueError("Invalid start code")

        # Data length: 2 Bytes, Little Endian
        self.length = struct.unpack('<H', self.frame[1:3])[0]

        # Function code: 1 Byte
        self.function_code = self.frame[3]

        # Address codes: 1 Byte each
        self.address_1 = self.frame[4]
        self.address_2 = self.frame[5]

        # Data: n Bytes
        data_length = self.length - 7  # Subtract header, length, command, addresses, checksum length
        self.data = self.frame[6:6 + data_length]

        # Checksum: 2 Bytes, Little Endian
        # self.checksum = struct.unpack('<H', self.frame[6 + data_length:8 + data_length])[0]

    def get_function_description(self):
        return self.FUNCTION_CODES.get(self.function_code, "Unknown Function")

    def __str__(self):
        return (
            f"Header: {hex(self.header)}\n"
            f"Length: {self.length}\n"
            f"Function Code: {hex(self.function_code)} ({self.get_function_description()})\n"
            f"Address 1: {hex(self.address_1)}\n"
            f"Address 2: {hex(self.address_2)}\n"
            f"Data: {self.data}\n"
            # f"Checksum: {hex(self.checksum)}"
        )

# # Example usage
# if __name__ == "__main__":
#     # Example frame string: '55 B 0 4 3 6 0 0 0 40 DC 65 \r\n'
#     frame_str = b'55 B 0 4 3 6 0 0 0 40 DC 65 \r\n'
#     parser = FrameParser(frame_str)
#     print(parser)

