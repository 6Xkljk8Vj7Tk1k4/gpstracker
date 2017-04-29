import socket
import sys
from thread import *

def parse_tracker_data(msg):
    # Validate it's a correct head and tail
    if not isinstance(msg, str):
        return "ERROR 01"
    if(len(msg) < 19):
        return "ERROR 02"
    if msg[0] != '(' and msg[len(msg) - 1] != ')':
        return "ERROR 03"

    identifier = msg[1:1+12]
    command = msg[13:13+4]

    if command == "BP00": # Heartbeet
        retval = '(' + identifier + 'AP01HSO)'+'\r\n'
        return retval

    elif command == "BR00": # Position
        # Date
        offset = 17
        offset_end = offset + 6
        date = msg[offset:offset_end]

        # Availability
        offset = offset_end
        offset_end = offset + 1
        availability = msg[offset:offset_end]

        # Latitude
        offset = offset_end
        offset_end = offset + 9
        latitude = msg[offset:offset_end]

        # Latitude indicator
        offset = offset_end
        offset_end = offset + 1
        latitude_ind = msg[offset:offset_end]

        # Longitude
        offset = offset_end
        offset_end = offset + 10
        longitude = msg[offset:offset_end]

        # Longitude Indicator
        offset = offset_end
        offset_end = offset + 1
        longitude_ind = msg[offset:offset_end]

        # Speed
        offset = offset_end
        offset_end = offset + 5
        speed = msg[offset:offset_end]

        # Time
        offset = offset_end
        offset_end = offset + 6
        times = msg[offset:offset_end]

        # Orientation
        offset = offset_end
        offset_end = offset + 6
        orientation = msg[offset:offset_end]

        # IOState
        offset = offset_end
        offset_end = offset + 8
        iostate = msg[offset:offset_end]

        # Milepost (L)
        offset = offset_end
        offset_end = offset + 1
        milepost = msg[offset:offset_end]

        # Mileage
        offset = offset_end
        offset_end = offset + 8
        mileage = msg[offset:offset_end]

        if availability == 'A':
            latitude_dd = round(float(latitude[0:2])  + float(latitude[2:2+7]) /60, 6)
            if latitude_ind != "N":
                latitude_dd = - latitude_dd

            longitude_dd = round(float(longitude[0:3]) + float(longitude[3:3+7])/60, 6)
            if longitude_ind != "E":
                longitude_dd = - longitude_dd

            maps_url = "http://maps.google.com/maps/?q=loc:" + str(latitude_dd) + "," + str(longitude_dd) + "&z=15"

            ret = ";OK" + ";IMEI:"      + identifier + \
                                                                        ";latitude:"  + str(latitude_dd) + \
                                                                        ";longitude:" + str(longitude_dd) + \
                                                                        ";speed:"     + speed + \
                                                                        ";date:"      + date + \
                                                                        ";time:"      + times + \
                                                                        '\r\n'

            with open("foo", "a") as f:
                f.write(ret)
        retval = '(' + identifier + 'AP05HSO)'+'\r\n'
    return retval

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8821 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        print data
        reply = parse_tracker_data(data)
        print reply
        if not data:
            break
        conn.sendall(reply)

    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
