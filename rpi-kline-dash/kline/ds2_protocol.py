"""BMW DS2 protocol frame building, checksum, and validation.

DS2 frame structure:
  [Address] [Length] [Payload ...] [Checksum]
  - Address: target ECU (0x12 for DME/MS41)
  - Length:  total bytes including address and checksum
  - Checksum: XOR of all preceding bytes
"""


def calc_checksum(data: bytes) -> int:
    """XOR checksum of all bytes."""
    xor = 0
    for b in data:
        xor ^= b
    return xor


def build_frame(address: int, payload: bytes) -> bytes:
    """Build a complete DS2 request frame.

    Args:
        address: ECU address (e.g. 0x12 for DME)
        payload: command bytes (without addr/len/checksum)

    Returns:
        Complete frame bytes ready to send.
    """
    total_len = len(payload) + 3  # addr + len + payload + checksum
    frame = bytes([address, total_len]) + payload
    chk = calc_checksum(frame)
    return frame + bytes([chk])


def validate_response(data: bytes, expected_addr: int = 0x12) -> bool:
    """Validate a DS2 response frame.

    Checks address, length field, and XOR checksum.
    """
    if len(data) < 3:
        return False
    if data[0] != expected_addr:
        return False
    if data[1] != len(data):
        return False
    expected_chk = calc_checksum(data[:-1])
    return expected_chk == data[-1]


def is_positive_ack(data: bytes) -> bool:
    """Check if response has positive ACK (0xA0) at byte 2."""
    return len(data) >= 3 and data[2] == 0xA0
