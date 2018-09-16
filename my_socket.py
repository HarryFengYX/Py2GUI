import socket
import json


class socket_server:
    def __init__(self, host, port, backlog=5, size=1024, ):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.size = size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.n = 0

        self.s.bind((host,port))
        self.s.listen(backlog)

    def stdop(self, dpf):
        self.accept_client()
        while 1:
            try:
                self.receive_data()
                self.process_data(dpf)
            except KeyboardInterrupt:
                self.close_client()
    
    def accept_client(self, ):
        self.client, address = self.s.accept()
        print("Client connected.")

    def receive_data(self, ):
        self.data = self.client.recv(self.size)
        print("Just received:", self.data.decode())

    def send(self, text):
        text = str(self.n) + ":" + text + "END_OF_CONNECTION"
        self.client.send(text.encode())
        self.n += 1
        # print("sent: %s" % text)

    def process_data(self, data_process_func):
        data_process_func(self.data, self.client)

    def close_client(self, ):
        self.client.close()
        print("Client closed")

def ping_pong_server(data, client):
    if data == b"ping\n":
        print ("Unity Sent: " + str(data))
        client.send(b"pong\n")
    else:
        client.send(b"Bye!\n")
        print ("Unity Sent Something Else: " + str(data))
        client.close()

if __name__ == '__main__':
    # ping pong test to unity
    ss = socket_server('localhost', 50000)
    ss.stdop(ping_pong_server)
