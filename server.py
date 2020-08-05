import socket
import json
from time import strftime, gmtime
from hakuCore.config import HOST, RECEIVEPORT, BUF_SIZE
from hakuCore.hakuCore import haku

ADDRESS = (HOST, RECEIVEPORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)
server_socket.listen(1)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

REPLY = "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 0\r\nServer: weilinfox-virHttp\r\n"

print("\nCtrl+C to quit.\n")

while True:
    try:    
        client_socket, address = server_socket.accept()
        #print(address)

        # 获取头
        postData = client_socket.recv(BUF_SIZE)
        postHead, postBody = postData.split(b"\r\n\r\n", 1);
        postHead = postHead.decode('utf-8')

        dataLength = 0  # 数据长度
        myId = 0        # bot的QQ ID
        for it in list(postHead.split("\r\n")):
            itmName, itmData = it.split(" ", 1)
            if itmName == "Content-Length:":
                dataLength = int(itmData)
            elif itmName == "X-Self-Id:":
                myId = int(itmData)

        # 超长数据
        while len(postBody) < dataLength:
            postData = client_socket.recv(BUF_SIZE)
            if (len(postData) == 0):
                break;
            postBody += postData

        # 响应
        timeStr = strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime())
        rplStr = REPLY + 'Date: ' + timeStr + "\r\n\r\n"
        client_socket.send(rplStr.encode('utf-8', errors='ignore'))

        postBody = postBody.decode('utf-8')
        print('\n[', timeStr, '](收到):', postBody)

        try:
            haku(json.loads(postBody))
        except:
            pass

    except KeyboardInterrupt:
        break
    except:
        pass


print("\n\nBye~\n")
server_socket.close()
