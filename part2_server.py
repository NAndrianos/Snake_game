# Group#: G37
# Student Names: Ryley McRae & Niko Andrianos

from socket import *
import random, time

"""
    Implements a server for a UDP Pinger application on a local host.
"""
class Server:
    def __init__(self, host: str = "127.0.0.1", port: int = 12000, bufferSize: int = 2048):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)

    def run(self):
        self.serverSocket.bind((self.host, self.port))
        print(f"The server is listening on port {self.port}")
        while True:
            message, clientAddress = self.serverSocket.recvfrom(self.bufferSize)
            ignoreMessageFlag = True if random.random() < 0.1 else False # create a flag with a 10% probability to simulate packet loss
            if ignoreMessageFlag is True:
                continue
            else:
                responseMessage = ' '.join(message.decode().split(' ')[:3]) + " ditto" # perform string manipulation to the desired format
                time.sleep(random.uniform(0.005, 0.050)) # sleep for 5 - 50ms before responding
                self.serverSocket.sendto(responseMessage.encode(), clientAddress) # send response


if __name__ == "__main__":
    server = Server()
    server.run()