def print_hex(prefix, data):
    print("{}: ".format(prefix), end="")
    for i in data:
        print("{:02x}".format(i), end="")
    print()