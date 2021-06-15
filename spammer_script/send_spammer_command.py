import socket
import json
import time

data_to_send = {
    "command": "add",
    "data": [
        {
            "id": 1,
            "s_type": "vk",
            "login": "1111",
            "target": {
                "t_type": "post",
                "current": 0,
                "total": 0
            },
        },
        {
            "id": 2,
            "s_type": "vk",
            "login": "1111",
            "target": {
                "t_type": "post",
                "current": 0,
                "total": 0
            }
        },
        {
            "id": 3,
            "s_type": "vk",
            "login": "1111",
            "target": {
                "t_type": "post",
                "current": 0,
                "total": 0
            }
        }
    ]
}

start = {
    "command": "start",
    "data": [1,2,3]
}

delete = {
    "command": "delete",
    "data": [2,4,6]
}

# s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# s.connect(('localhost', 9000))
# command = json.dumps(data_to_send).encode('utf-8')
# s.send(command)
# print('send add command')
# time.sleep(5)
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.connect(('localhost', 9000))
command = json.dumps(delete).encode('utf-8')
s.send(command)
print('send start command')

