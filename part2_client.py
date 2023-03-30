# Group#: G37
# Student Names: Ryley McRae & Niko Andrianos

"""
    This program implements a client for a UDP Pinger 
    application on a local host.
"""

from socket import *
import time

if __name__ == "__main__":
    # Pre-define a list of messages to ping the server with
    messageList = [
        "PING 1 - hello world!",
        "PING 2 - what is your name?",
        "PING 3 - SPAM12345",
        "PING 4 - 99999900009999999",
        "PING 5 - ______^^^^^__===------         ___"
    ]

    # Create variables to idenfity the server
    serverName = "localhost"
    serverPortParams = ("127.0.0.1", 12000)
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # Set a timeout for 1 second while client waits for serve
    clientSocket.settimeout(1.0)

    # Ping the server once with each message
    for message in messageList:
        
        # Start RTT time tracker
        messageTimerStart = time.time()

        # Send message over port
        clientSocket.sendto(message.encode(), serverPortParams)

        # Use a try/except to handle a timeout from the server side
        try:
            # Read reply
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        
            # End RTT time tracker
            messageTimerEnd = time.time()

            # Calculate the RTT
            roundTripTime = messageTimerEnd - messageTimerStart

            # Print reply and RTT for the message
            print(f"The recieved message: {modifiedMessage.decode()}\nThe RTT for the message: {roundTripTime} Seconds")

        except timeout:
            # If no reply is avaliable print the timeout message
            print("request timed out")

    # Close client after each message is sent
    clientSocket.close()