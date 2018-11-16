def print_hex(prefix, data):
    print("{}: ".format(prefix), end="")
    for i in data:
        print("{:02x}".format(i), end="")
    print()

def read_data(data):
    bin_data = None
    try:
        bin_data = bytearray.fromhex(data)
    except Exception as e:
        print(e)
    return bin_data