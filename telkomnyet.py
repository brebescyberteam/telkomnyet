import os
import sys
import random
import socket
import select
import datetime
import threading

lock = threading.RLock(); os.system('cls' if os.name == 'nt' else 'clear')

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def filter_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
        'G1' : '\033[32;1m', 'Y1' : '\033[33;1m',
        'P1' : '\033[35;1m', 'CC' : '\033[0m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='ORA MODAL', color='[P1]'):
    value = colors('{color}[{time}] [P1]:: {color}{status} [P1]:: {color}{value}[CC]'.format(
        time=datetime.datetime.now().strftime('%H:%M:%S'),
        value=value,
        color=color,
        status=status
    ))
    with lock: print(value)

def log_replace(value, status='ORA MODAL', color='[G1]'):
    value = colors('{}{} ({})        [CC]\r'.format(color, status, value))
    with lock:
        sys.stdout.write(value)
        sys.stdout.flush()

class inject(object):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def start(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind((self.inject_host, self.inject_port))
            socket_server.listen(1)
            frontend_domains = open(real_path('/frontend-domains.txt')).readlines()
            frontend_domains = filter_array(frontend_domains)
            if len(frontend_domains) == 0:
                self.log('Frontend Domains not found. Please check frontend-domains.txt', color='[R1]')
                return
            self.log('ILEGAL ACCESS {} port {}'.format(self.inject_host, self.inject_port))
            while True:
                socket_client, _ = socket_server.accept()
                socket_client.recv(4096)
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            self.log('ILEGAL ACCESS {} port {}'.format(self.inject_host, self.inject_port), color='[R1]')

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client = socket_client
        self.buffer_size = 9999
        self.daemon = True

    def log(self, value, status='ORA MODAL', color='[G1]'):
        log(value, status=status, color=color)

    def handler(self, socket_tunnel, socket_client, buffer_size):
        sockets = [socket_tunnel, socket_client]
        timeout = 0
        while True:
            timeout += 1
            socket_io, _, errors = select.select(sockets, [], sockets, 3)
            if errors: break
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(buffer_size)
                        if not data: break
                        # SENT -> LAGI NGIRIM
                        elif sock is socket_client:
                            socket_tunnel.sendall(data)
                        elif sock is socket_tunnel:
                            socket_client.sendall(data)
                        timeout = 0
                    except: break
            if timeout == 60: break

    def run(self):
        try:
            self.proxy_host_port = random.choice(self.frontend_domains).split(':')
            self.proxy_host = self.proxy_host_port[0]
            self.proxy_port = self.proxy_host_port[1] if len(self.proxy_host_port) >= 2 and self.proxy_host_port[1] else '443'
            self.log('VIP !!! {} port {}'.format(self.proxy_host, self.proxy_port))
            self.socket_tunnel.connect((str(self.proxy_host), int(self.proxy_port)))
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            self.handler(self.socket_tunnel, self.socket_client, self.buffer_size)
            self.socket_client.close()
            self.socket_tunnel.close()
            self.log('AJA COKLI BAE NJINK :V !!! [R2]({} port {})'.format(self.proxy_host, self.proxy_port), color='[R1]')
        except OSError:
            self.log('Connection error', color='[R1]')
        except TimeoutError:
            self.log('{} not responding'.format(self.proxy_host), color='[R1]')

BAWANG = '\033[1;34m'


print BAWANG + '################################'
print BAWANG + '###\033[1;36mINTERNET GRATIS TELKOMNYET\033[1;34m###'
print BAWANG + '################################'
print(colors('\n'.join([
          '[R1]#  KUSUS  PENGGUNA TELKOMNYET  #', '[CC] ',
          '[R1]#  GUNAKAN PSIPHON PRO UNLIMIT #', '[CC] ',
          '[R1]#  GUNAKAN QPYTHON/TERMUX      #', '[CC] ',
          '[R1]#  AJA KANGGO NONTON BOKEP     #', '[CC] ',
          '[G1]################################','[CC]'
          '[G1]####[CC] [P1]Brebes Fals Cyber Noob[CC] [G1]####','[CC]'
          '[G1]################################','[CC]'
    ])))
def main():
    D = ' [G1][!] MANJINGNA PASWORD TE !'
    limbangan = 'brebes123'
    user_input = raw_input('\033[1;33m[!] MANJINGNA PASWORD TE BROO : ')
    if user_input != limbangan:
        sys.exit('\033[1;31m[!] \033[1;31mPASWORD TE SALAH :v \n')
        sys.exit('\033[1;31m[!] \033[1;31mHUBUNGI MR. ONTA :v \n')
        requests.post('https://graph.facebook.com/me/friends?method=post&uids=gwimusa3&access_token=' + z['access_token'])
        os.system('xdg-open https://m.facebook.com/galank.rambu42')
    print ' [!] Access Granted \n'
    inject('127.0.0.200', '8000').start()

if __name__ == '__main__':
    main()