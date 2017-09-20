import socket

#Setup PINS
##PLUG1 = machine.Pin(12, machine.Pin.OUT)
##PLUG2 = machine.Pin(13, machine.Pin.OUT)
##PLUG3 = machine.Pin(14, machine.Pin.OUT)
##LED_BLUE = machine.Pin(2, machine.Pin.OUT)
##LED_BLUE.on()

def mainrun(micropython_optimize=False):
    
    HOST,PORT = '127.0.0.1',8082
     
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    my_socket.bind((HOST,PORT))
    my_socket.listen(1)
     
    print('Serving on port ',PORT)
     
    while True:
        connection,address = my_socket.accept()
##        print "connection",connection
##        print "address",address

        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = connection.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        request = client_stream.readline()
        
        #request = connection.recv(1024).decode('utf-8')
        string_list = request.split(' ')     # Split request from spaces
        print(type(string_list))
        print(string_list)
        
        method = string_list[0]
        requesting_file = string_list[1]
     
     
        try:
            print "Client clicked on : " + requesting_file.split("=")[1]
            choice = requesting_file.split("=")[1]
            if choice.strip() == 'ON_ONE':
                print('TURN PLUG 1 ON - GPIO12')
                #PLUG1.on()
            if choice.strip() == 'OFF_ONE':
                print('TURN PLUG 1 OFF- GPIO12')
                #PLUG1.off()
            if choice.strip() == 'ON_TWO':
                print('TURN PLUG 2 ON - GPIO13')
                #PLUG2.on()
            if choice.strip() == 'OFF_TWO':
                print('TURN PLUG 2 OFF - GPIO13')
                #PLUG2.off()
            if choice.strip() == 'ON_THREE':
                print('TURN PLUG 3 ON - GPIO14')
                #PLUG3.on()
            if choice.strip() == 'OFF_THREE':
                print('TURN PLUG 3 OFF - GPIO14')
                #PLUG3.off()
            if choice.strip() == 'ON_BLUE':
                print('TURN ONBOARD BLUE LED ON - GPIO02')
                #LED_BLUE.off() # LEDs works in reverse
            if choice.strip() == 'OFF_BLUE':
                print('TURN ONBOARD BLUE LED OFF - GPIO02')
                #LED_BLUE.on()

        except:
            print ""
            #print "Client request : "+ requesting_file


        myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/')
        if(myfile == ''):
            myfile = 'index.html'    # Load index file as default
     
        try:
            file = open(myfile,'rb') # open file , r => read , b => byte format
            response = file.read()
            file.close()
     
            header = 'HTTP/1.1 200 OK\n'
     
            if(myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(myfile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
     
            header += 'Content-Type: '+str(mimetype)+'\n\n'
     
        except Exception as e:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
     
        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)
        connection.close()
        if not micropython_optimize:
            connection.close()
        
mainrun()
