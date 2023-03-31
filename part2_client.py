# Group#: G37
# Student Names: Ryley McRae & Niko Andrianos

from socket import *
import time

"""
    Implements a client for a UDP Pinger application on a local host.
"""
class Client:
    def __init__(self, serverName: str = "localhost", serverPort: int = 12000, bufferSize: int = 2048):
        self.serverName = serverName
        self.serverPort = serverPort
        self.bufferSize = bufferSize
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1.0) # timeout exception will be raised 1 second after trying to receive data
    
    def close(self):
        self.clientSocket.close()

    def ping(self, request: str):
        try: # use a try/except to handle a timeout from the server side
            tripStartTime = time.time() # save the time of right before the request is made
            self.clientSocket.sendto(message.encode(), (self.serverName, self.serverPort)) # send request to server
            response, serverAddress = self.clientSocket.recvfrom(self.bufferSize) # fetch the response
            roundTripTime = round(1000 * (time.time() - tripStartTime), 3) # calculate the round-trip-time in ms
            print(f"Request:\t{request}\nResponse:\t{response.decode()}\nRound trip:\t{roundTripTime}ms")
        except timeout:
            print("Request timed out")
        except Exception:
            print("Unknown exception occurred")


if __name__ == "__main__":
    # Pre-define a list of messages to ping the server with
    messages = [
        "PING 1 - hello world!",
        "PING 2 - what is your name?",
        "PING 3 -    SPAM12345",
        "PING 4 - 99999900009999999",
        "PING 5 - ______^^^^^__===------         ___"
    ]

    client = Client()
    for message in messages:
        client.ping(message)
        print("----")
    client.close()