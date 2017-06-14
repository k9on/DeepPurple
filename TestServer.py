# encoding : UTF-8
from socket import *

def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("127.0.0.1", 30005))    # bind 및 connect 에는  반드시 튜플 형식으로 와야됨
    server.listen(5)
    conn, addr = server.accept()
    while 1:
        #data = conn.recv(1024)
        a = input("input : ")
        conn.send(a.encode(encoding='UTF-8'))
    conn.close()

if __name__ == "__main__":
    main()
