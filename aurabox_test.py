from util import *
from aurabox import *
from bluetooth import *
import sys

addr = None
mock = False

if len(sys.argv) < 2:
    print("No device specified. Searching all nearby bluetooth devices for the SPP service")
else:
    addr = sys.argv[1]
    print("Searching for a SPP on %s" % addr)

if not mock:
    service_matches = find_service( address = addr )

    if len(service_matches) == 0:
        print("Couldn't find the SPP service.")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    sock = BluetoothSocket( RFCOMM )
    sock.connect((host, port))

print("connected.  type stuff")
while True:
    data = input()
    if len(data) == 0: 
        break

    bin_data = None
    
    # Rudimentary command parsing
    cmd = data[0]
    data = data[1:]
    if cmd == 'r': 
        print("raw")
        bin_data = read_data(data)
        print (bin_data)
    elif cmd == 'i':
        header = img_header()
        payload = read_data(data)
        if payload is None: continue
        bin_data = header + payload
        bin_data = bin_data + checksum(bin_data[1:])
        bin_data.append(0x02)

        # Writing to output buffer
        out_buffer = escape_message(bin_data)   
        
        bin_data = out_buffer
    else:
        print ("nope")

    # Only bother if there is data to be sent
    if bin_data == None:
        continue

    try:
        if not mock:
            sock.send(bytes(bin_data))
    except Exception as e:
        print(e)

if not mock:
    sock.close()