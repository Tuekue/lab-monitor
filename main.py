import ujson
from dataclasses import dataclass, field
import socket
import pprint
import sys

server_host  = '192.168.1.101'
server_port = 8765
socket.setdefaulttimeout(3)

@dataclass
class HostInfo:
    hostname : str
    ipaddr : str
    cpu : str
    ram : str
    disks : list[str] = field(default_factory=str)
    def toJson(self):
    #    Serialize the object custom object
        return ujson.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

hosts: dict[str,HostInfo] = {}

def readJson():
    with open("hosts.json", "r", encoding="utf-8") as file:
        data = ujson.load(file)
        for datum in data:
            hostData = HostInfo(**datum)
            hosts[hostData.ipaddr] = hostData

def checkSocket(ipofserver):
    print('in checksoket', ipofserver)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as msg:
        err = msg
        sock = None
#       sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      #For server ?
    try:
        sock.settimeout(1)   # 1 second timeout
        sock.connect((ipofserver,server_port))
    except OSError as msg:
        err = msg
        sock.close()
        sock = None
    if sock is None:
        print('Could not open socket: ',err)
        #sys.exit(1)
    else:
        with sock:
            sock.sendall(b"SEND")
            sockData = sock.recv(1024)
            sockData = ujson.loads(sockData)
            hostData = HostInfo(**sockData)
            hosts[hostData.ipaddr] = hostData

        # for datum in sockData:
        #     print("sokData: ",sockData)
        #     print("Datum: ", datum)
        #     hostData = HostInfo(*datum)
        #     hosts[hostData.ipaddr] = hostData

ips={'192.168.1.101', '10.1.1.14', '192.168.1.102', '10.1.1.254'}

if __name__ == '__main__':
#    main()
#    readJson()
#    for host in hosts:
#        print(host)
    for ipaddr in ips:
        print(ipaddr)
        checkSocket(ipaddr)
#    print(ujson.dumps(hosts, indent=2))
    pprint.pprint(hosts)
