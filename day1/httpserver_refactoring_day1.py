from socket import *
import json
import re
from enum import Enum
from dataclasses import dataclass

class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'

class HTTPStatusCode(Enum):
    OK = (200, 'OK')
    NOT_FOUND = (404, 'Not Found')
    SEE_OTHER = (303, 'See Other')
    SERVER_ERROR = (500, 'Internal Server Error')

class HttpContentType(Enum):
    TEXT_HTML = 'text/html'
    APPLICATION_JSON = 'application/json'
    IMAGE_PNG = 'image/png'

@dataclass
class HTTPRequest:
    method: HTTPMethod
    url: str
    path: str
    query: dict = None

# 정규표현식으로 url을 파싱
def parseQuery(url: str) -> tuple[str, dict | None]:
    # (\/[\w\-.\/]*)+([/#]*)([0-9a-zA-Z\-]*)\?*(.*)
    # https://regexr.com/
    path = url
    query = {}
    match = re.search(r'(\/[\w\-.\/]*)+([/#]*)([0-9a-zA-Z\-]*)\?*(.*)', url)
    if match:
        # 매칭된 그룹의 개수를 출력
        print(len(match.groups()))
        # 경로를 추출
        path = match.group(1)
        # 쿼리 문자열을 추출
        queryStr = match.group(4)
        # 만약 입력 경로의 끝이 '/'으로 끝나는 경우 제거
        if path[-1] == '/':
            path = path[:-1]
        # 입력 경로가 적히지 않은 경우 /으로 대체
        if path == '':
            path = '/'
        # &을 기준으로 1번 분할하고, =을 기준으로 다시 분할해서
        # 2개의 값을 가지고 key와 data로 dictionary를 구성
        for q in queryStr.split('&'):
            arQs = q.split('=')
            if len(arQs) == 2:
                query[arQs[0]] = arQs[1]
    return path, query

# str이 아니라 HTTPRequest로 return값을 변경
# method, url, path, query로 나누어짐.
def parseRequest(requests: str) -> HTTPRequest | None:
    if len(requests) < 1:
        return None
    arRequests = requests.split('\n')
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1', line)
        if match:
            method = HTTPMethod(match.group(1))
            url = match.group(2)
            path, query = parseQuery(url)
            try:
                return HTTPRequest(method, url, path, query)
            except ValueError:
                return None
    return None

# 응답문을 간단하게 변경
# HTTP/1.1 응답번호 응답번호에 대한 설명(200 OK)
# Content-Type : html/image/location등... 
def makeResponseHeader(status: HTTPStatusCode, contentType: HttpContentType, extra: dict|None = None) -> str:
    strResp = f'HTTP/1.1 {status.value[0]} {status.value[1]}\n'
    strResp += f'Content-Type: {contentType.value}\n'
    if extra:
        for key, value in extra.items():
            strResp += f'{key}: {value}\n'
    strResp += '\n'
    return strResp

def getUserList() -> None:
    return [
        {'id': 1, 'name': 'Trump'},
        {'id': 2, 'name': 'Biden'},
        {'id': 3, 'name': 'Obama'},
    ]

# 각 요청의 응답에 대한 핸들러 함수들
# 응답은 바이트 형식으로 보내기 때문에, return값이 bytes
# /
def handler_home(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.TEXT_HTML)
    response += '<html><body>Hello World<br /><img src="/google.png" /></body></html>\n'
    return response.encode('utf-8')

# /user/list
def handler_user_list(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.APPLICATION_JSON)
    response += json.dumps(getUserList())
    return response.encode('utf-8')

# /google
def handler_google(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.SEE_OTHER, HttpContentType.TEXT_HTML, {'Location': 'https://www.google.com'})
    return response.encode('utf-8')

# /google.png
def handler_google_png(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.IMAGE_PNG).encode('utf-8')
    # png파일을 그대로 읽어서 바이트 형태로 출력
    with open('google.png', 'rb') as f:
        response += f.read()
    return response

def hander_404(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.NOT_FOUND, HttpContentType.TEXT_HTML)
    response += '<html><body>404 Not Found</body></html>\n'
    return response.encode('utf-8')

def createServer():
    arPath = ['/', '/user/list', '/google.png', '/google']
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(4096).decode('utf-8')
            print(request)
            req = parseRequest(request)
            # 만약 요청이 제대로 들어오지 않은 경우 shutdown
            if req is None or req.url is None:
                connectionSocket.shutdown(SHUT_WR)
                continue
            print(req)
            resp = None
            
            # 핸들러 함수를 사용해서 각 url에 대한 응답을 수행
            if not req.path.startswith(tuple(arPath)):
                resp = hander_404(req)
            elif req.path == '/google':
                resp = handler_google(req)
            elif req.path == '/user/list':
                resp = handler_user_list(req)
            elif req.path == '/':
                resp = handler_home(req)
            elif req.path == '/google.png':
                resp = handler_google_png(req)
            
            # 보내야 하는 응답의 크기가 어느정도인지 모름
            # 1024를 한 청크 사이즈로 설정해서, 청크 사이즈씩 계속해서 데이터를 읽어서 arChunks로 설정
            # 이후 chunk(1024bytes)크기만큼 출력
            if resp is not None:
                chunk_size = 1024
                arChunks = [resp[i:i+chunk_size] for i in range(0, len(resp), chunk_size)]
                for chunk in arChunks:
                    connectionSocket.sendall(chunk)
            connectionSocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
    except Exception as e:
        print('Unexpected error:', e)
        
if __name__ == '__main__':
    createServer()