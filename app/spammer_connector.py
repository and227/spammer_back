import socket
from core.config import settings
from fastapi.encoders import jsonable_encoder

def connect_spammer_socket():
    try:
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((settings.SPAMMER_SERVER, settings.SPAMMER_PORT))
        yield s
        s.close()
    except socket.timeout as err:
        return None

def send_spammer_command(sock, command):
    try: 
        sock.send(jsonable_encoder(command))
        answer = sock.recv(1024)
    except socket.timeout as err:
        return None
    else:
        return answer