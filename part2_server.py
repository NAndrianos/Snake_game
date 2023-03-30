# Group#: G37
# Student Names: Ryley McRae & Niko Andrianos

"""
    This program implements a server for a UDP Pinger 
    application on a local host.
"""

from socket import *
import random
import time

if __name__ == "__main__":
    # Create variables to set up server
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Bind to specified port
    serverSocket.bind(("127.0.0.1", serverPort))

    print("The server is ready to recieve!")

    # Unlessed process is killed, let the server listen
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)

        # Create a flag with a 10% probability to simulate packet loss
        ignoreMessageFlag = True if random.random() < 0.1 else False

        # Skip this iteration: 'drop the packet'
        if ignoreMessageFlag is True:
            continue
        
        # Perform string manipulation to the desired format
        decodedMessageList = message.decode().split(" ")
        responseMessage = f"{decodedMessageList[0]} {decodedMessageList[1]} - ditto"

        # Generate a random sleep time between 5 and 50 milliseconds
        sleepTime = random.uniform(0.005, 0.05)
        time.sleep(sleepTime)

        # Reply to the client with response message
        serverSocket.sendto(responseMessage.encode(), clientAddress)