# Dont forget to add port to firewall
# sudo firewall-cmd --permanent --add-port=8765/tcp 

import json
import socket
import psutil
import time

from dataclasses import dataclass, field

server_host = "localhost"
server_port = 8765

@dataclass
class HostInfo:
    hostname : str
    ipaddr : str
    cpu : str
    ram : str
    disks : list[str] = field(default_factory=str)

    def toJson(self):
    #    Serialize the object custom object
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    
def hostInfo():
    hostname=socket.gethostname()
    ip=get_ip()
    cpu=psutil.Process().cpu_percent()
    mem=psutil.virtual_memory().percent
    disks: dict[str,str] = {}
    for part in psutil.disk_partitions(all=False):
        disks[part.device] = int(psutil.disk_usage(part.mountpoint).percent)
    readInfo = HostInfo(hostname,ip,cpu,mem,disks)
    print(readInfo)
    print(readInfo.toJson())
    return readInfo.toJson()

def start_server(server_host, server_port):
    ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
#        ServerSocket.bind((server_host, server_port))
        ServerSocket.bind(('', server_port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {get_ip()}:{server_port}...')
    ServerSocket.listen()

    while True:
        connection, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        with connection:
            data = connection.recv(1024)
            message = data.decode('utf-8')
            if message == 'END':
                print('Server closed')
                break
            if message == 'SEND':
                connection.send(str.encode(hostInfo()))
                time.sleep(1)
        connection.close()
    ServerSocket.close()

def main():
    start_server(server_host, server_port)

if __name__ == "__main__":
    main()


    
