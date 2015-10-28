# Python port scanner implementation based on the book violent python
# Four steps to construct a port scanneer
# 1. input a hostname and a comma separated list of ports to scan.
# 2. we will translate the hostname into an IPv4 Internet address.
# 3. For each port in the list, connect to the target address and specific
# port. 
# 4. Send garbage data and read the banner results sent back by the specific
# application.

import argparse
from socket import *
from threading import *
screenLock = Semaphore(value=1)

def main():
    #init the parser
    parser = argparse.ArgumentParser(description="Scanning the availablity of port(s) in hostname(s)")
    #taking the arguments
    parser.add_argument("H", nargs='+', help="Target Hostname(s)")
    parser.add_argument("-p", "--portnumber", nargs='+', help="Target Port Number(s)")
    #parsing the arguments
    args = parser.parse_args()
    #initialize target hostname and target port number(s)
    target_hosts = args.H
    target_ports = []
    if args.portnumber:
        target_ports = [map(int, port.split(",")) for port in args.portnumber]
    #if the target port isn't specify, then assume all ports.
    if len(target_hosts) > len(target_ports):
        [target_ports.append(range(0,65535)) for i in range(len(target_hosts) - len(target_ports))]
    #validate input    
    validate_inputs(target_hosts, target_ports)
    #port scan
    for i in range(len(target_hosts)):
        portScan(target_hosts[i], target_ports[i])

def validate_inputs(target_hosts, target_ports):
    '''Validate the input hosts and ports return none'''
    #ensure the number of host matches the number of port sequence
    if len(target_hosts) < len(target_ports):
        raise ValueError, "Insufficient host names, target ports > target hosts"    
    #validate the input hostname(s)
    for host in target_hosts:
        try:
            inet_aton(host)
        except error:
            raise ValueError, "%s not a valid hostname" %host
    #validate the input port(s)
    for ports in target_ports:
        for port in ports:
            if port not in range(0,65535): 
                raise ValueError, "%d not a valid port. Port number has to be between 0-65535" %port
            
def connect(hostname, port):
    '''make a connection to the host by the specified port'''
    try:
        conn_sock = socket(AF_INET, SOCK_STREAM)
        conn_sock.connect((hostname, port))
        conn_sock.send('Hello world!\r\n')
        results =  conn_sock.recv(100)
        screenLock.acquire()        
        print "%d  TCP port open" %port
        connSkt.close()
    except:
        screenLock.acquire()
        print "%d TCP port closed" %port
    finally:
        screenLock.release()
        conn_sock.close()

def portScan(hostname, ports):
    '''perform port scanning'''
    try:
        hostIP = gethostbyname(hostname)
    except:
        print "Unknown host"%hostname
        return
    try:
        name = gethostbyaddr(hostIP)
        print '\n Scan Results for: ' + name[0]
    except:
        print '\n Scan Results for: ' + hostIP
        setdefaulttimeout(1)
        #threading
        for port in ports:
            t = Thread(target=connect, args=(hostname, int(port)))
            t.start()
    

if __name__ == "__main__":
    main()
