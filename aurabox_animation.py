from aurabox import checksum, escape_message, img_header
from bluetooth import find_service, BluetoothSocket, RFCOMM
from time import sleep
import sys

addr = None
mock = False

frames = []
zero = 0x01
one = 0x10
whatever = 0x00
for red in range(0, 100):
    frame = [whatever] * 50
    frame[red // 2] = one if red % 2 else zero
    frame = bytearray(frame)
    frames.append(frame)
    
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
keep_going = True
while keep_going:
    print ("click")
    for frame in frames:
        if len(frame) == 0: 
            break

        bin_data = None
        
        header = img_header()
        payload = frame
        if payload is None: continue
        bin_data = header + payload
        bin_data = bin_data + checksum(bin_data[1:])
        bin_data.append(0x02)

        # Writing to output buffer
        out_buffer = escape_message(bin_data)

        # Only bother if there is data to be sent
        if out_buffer == None: continue

        try:
            if not mock:
                sock.send(bytes(out_buffer))
                sleep(50/1000)
        except Exception as e:
            print(e)

if not mock:
    sock.close()