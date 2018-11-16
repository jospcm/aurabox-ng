def img_header():
    return bytearray([0x01, 0x39, 0x00, 0x44, 0x00, 0x0a, 0x0a, 0x04])

def checksum(data):
    """ Calculates the checksum, given a message without the STX and ETX.
    Returns a list with the ordered checksum bytes"""
    calc_sum = 0
    for i in data:
        calc_sum += i

    low_sum = calc_sum >> 8 & 0xFF
    high_sum = calc_sum & 0xFF
    return bytearray([high_sum, low_sum])

def escape_byte(data):
    """ Escapes (or not) a character 
    returns a list with the correct values """
    if data not in (1, 2, 3):
        return [data]
    return [3, data + 3]

def escape_message(msg):
    """ Escapes the applicable fields of a message. Expects the full message, returns the full message """
    out_buffer = bytearray([0x01])
    for elm in msg[1:-1]:
        out_buffer.extend(escape_byte(elm))
    out_buffer.append(0x02)
    return out_buffer
