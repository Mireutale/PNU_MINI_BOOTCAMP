from socket import *
import json
# 정규표현식 도구
import re

DB = [
    {'id': 1, 'name': 'Trump'},
    {'id': 2, 'name': 'Biden'},
    {'id': 3, 'name': 'Obama'}
]

def get_user_from_db():
    return DB

def parseRequest(requests: str) -> str | None:
    if len(requests) < 1:
        return None
    
    arRequests = requests.split('\n')
    # 사용자의 요청 명령어를 한줄씩 잘라서, 패턴을 검사.
    # 매치가 된 패턴을 출력
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1', line)
        if match:
            strMethod = match.group(1)
            print(strMethod)
            strPath = match.group(2)
            return strPath
    return None

def createServer():
    arPath = ['/', '/users', '/google.png', '/google']
    # IPv4, TCP 소켓
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            # 연결 요청을 받음.
            (connectionSocket, addr) = serverSocket.accept()
            print('Connection received from ', addr)
            
            # 연결된 호스트로부터 요청을 받음
            request = connectionSocket.recv(1024).decode('utf-8')
            print(request)
            strPath = parseRequest(request)
            print(f'Paht = {strPath}')
            response: str = ''
            if strPath is None:
                connectionSocket.shutdown(SHUT_WR)
                continue
            if strPath not in arPath:
                response = 'HTTP/1.1 404 Not Found\n'
                response += 'Content-Type: text/html\n'
                response += '\n'
                response += '<html><body>404 Not Found</body></html>\n'
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            if strPath == '/users':
                users = get_user_from_db()
                response = 'HTTP/1.1 200 OK\n'
                response += 'Content-Type: application/json; utf-8\n'
                response += '\n'
                # response += '<html><body>users DB</body></html>\n'
                # 위 데이터를 넣으면 json파일과 text파일이 합쳐져서 문제가 발생
                response += json.dumps(users)
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            elif strPath == '/google.png':
                response = 'HTTP/1.1 200 OK\n'
                response += 'Content-Type: image/png\n'
                response += '\n'
                connectionSocket.sendall(response.encode('utf-8'))
                with open ('google.png', 'rb') as f:
                    while chunk := f.read(1024):
                        connectionSocket.sendall(chunk)
                connectionSocket.shutdown(SHUT_WR)
                continue
            elif strPath == '/google':
                response = 'HTTP/1.1 303 See Other\n'
                response += 'Location: https://www.google.com/\n'  # 'http://' 대신 'https://' 사용
                response += 'Connection: close\n'  # 연결을 명확히 종료
                response += '\n'
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            else:
                response = 'HTTP/1.1 500 Internal Server Error\n'
                response += 'Content-Type: text/html\n'
                response += '\n'
                response += '<html><body>Hello this server is made by Mireutale</body></html>\n'
                connectionSocket.sendall(response.encode('utf-8'))
                #메세지를 주고받으면 연결 종료
                connectionSocket.shutdown(SHUT_WR)
            
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
        
if __name__ == '__main__':
    createServer()