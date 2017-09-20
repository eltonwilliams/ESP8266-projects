try:
    import usocket as socket
except:
    import socket
import machine
import network


CONTENT = b"""\
HTTP/1.0 200 OK


    <!DOCTYPE html>
    <html>
    <head> <title>WIFI Muliplug Control Interface</title> </head>
    <center><h1>WIFI Muliplug Control Interface</h1></center>
    <center><img src="plug_layout.jpg" alt="Multiplug Layout" style="width:800px;height:228px;"></center>
    <br>
    <br>
    <br>
    <center><form>
    PLUG 1:
    <button name="PLUG1" value="ON_ONE" type="submit">PLUG ON</button>
    <button name="PLUG1" value="OFF_ONE" type="submit">PLUG OFF</button><br><br>
    PLUG 2:
    <button name="PLUG2" value="ON_TWO" type="submit">PLUG ON</button>
    <button name="PLUG2" value="OFF_TWO" type="submit">PLUG OFF</button><br><br>
    PLUG 3:
    <button name="PLUG3" value="ON_THREE" type="submit">PLUG ON</button>
    <button name="PLUG4" value="OFF_THREE" type="submit">PLUG OFF</button><br><br>
    LED BLUE:
    <button name="LEDB" value="ON_BLUE" type="submit">LED ON</button>
    <button name="LEDB" value="OFF_BLUE" type="submit">LED OFF</button>
    </form></center>
    </html>

"""

#Setup PINS
PLUG1 = machine.Pin(12, machine.Pin.OUT)
PLUG2 = machine.Pin(13, machine.Pin.OUT)
PLUG3 = machine.Pin(14, machine.Pin.OUT)
LED_BLUE = machine.Pin(2, machine.Pin.OUT)
LED_BLUE.on()

def mainrun(micropython_optimize=False):
    s = socket.socket()

    nic = network.WLAN(network.AP_IF)
    HOST = (nic.ifconfig())[0]
    PORT = 8080
    
    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo(HOST, PORT)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5) # up to 5 connections
    print("Listening, connect your browser to --> http://%s:%s" % (HOST,PORT))

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client connected from IP:", client_addr[0])


        if not micropython_optimize:
            client_stream = client_sock.makefile("rwb")
        else:
            client_stream = client_sock


        req = client_stream.readline()
        print("Request: %s" % req)

        string_list = (req.decode('utf-8')).split(' ')     # Split request from spaces
  
        method = string_list[0]
        requesting_file = string_list[1]
        
        try:
            choice = requesting_file.split("=")[1]
            print('Clicked on '+choice)
            if choice.strip() == 'ON_ONE':
                print('TURN PLUG 1 ON - GPIO12')
                PLUG1.on()
            if choice.strip() == 'OFF_ONE':
                print('TURN PLUG 1 OFF- GPIO12')
                PLUG1.off()
            if choice.strip() == 'ON_TWO':
                print('TURN PLUG 2 ON - GPIO13')
                PLUG2.on()
            if choice.strip() == 'OFF_TWO':
                print('TURN PLUG 2 OFF - GPIO13')
                PLUG2.off()
            if choice.strip() == 'ON_THREE':
                print('TURN PLUG 3 ON - GPIO14')
                PLUG3.on()
            if choice.strip() == 'OFF_THREE':
                print('TURN PLUG 3 OFF - GPIO14')
                PLUG3.off()
            if choice.strip() == 'ON_BLUE':
                print('TURN ONBOARD BLUE LED ON - GPIO02')
                LED_BLUE.off() # LEDs works in reverse
            if choice.strip() == 'OFF_BLUE':
                print('TURN ONBOARD BLUE LED OFF - GPIO02')
                LED_BLUE.on()

        except:
            print('')
       
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break

        client_stream.write(CONTENT)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()

mainrun()
